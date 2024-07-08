from django.contrib.auth.models import Group
from django.http import HttpResponseNotFound, HttpResponse
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from prodotti.forms import OrdineForm
from prodotti.models import Prodotto
from utenti.models import CustomUser, Venditore, Acquirente


# Create your tests here.

class OrdineTest(TestCase):
    def setUp(self):
        gruppo_acquirenti = Group.objects.create(name="Acquirenti")
        gruppo_venditori = Group.objects.create(name="Venditori")

        self.account_acquirente = CustomUser.objects.create_user(username="Acquirente di test", password="password")
        self.acquirente = Acquirente.objects.create(user=self.account_acquirente, nome=self.account_acquirente.username)
        self.account_acquirente.groups.add(gruppo_acquirenti)

        self.account_venditore = CustomUser.objects.create_user(username="Venditore di test", password="password")
        self.venditore = Venditore.objects.create(user=self.account_venditore, nome=self.account_venditore.username)
        self.account_venditore.groups.add(gruppo_venditori)

        self.prodotto = Prodotto.objects.create(titolo="Prodotto di test", prezzo=19.99, data_rilascio=timezone.now().date(), venditore=self.venditore)

        self.client = Client()
        self.client.login(username=self.account_acquirente.username, password="password")

    def test_ordine_utente_non_loggato(self):
        """
        Caso in cui l'utente che vuole fare l'ordine non è loggato
        """
        self.client.logout()

        url = reverse("ordine", kwargs={"pk": self.prodotto.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn(self.acquirente, self.prodotto.acquirenti.all())
        self.assertNotIn(self.prodotto, self.acquirente.prodotti.all())

    def test_ordine_utente_loggato_non_in_gruppo_acquirenti(self):
        """
        Caso in cui l'utente che vuole fare l'ordine è loggato ma non è nel gruppo Acquirenti
        """
        self.client.logout()
        self.client.login(username=self.account_venditore.username, password="password")

        url = reverse("ordine", kwargs={"pk": self.prodotto.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn(self.venditore, self.prodotto.acquirenti.all())

    def test_ordine_prodotto_specificato_non_esistente(self):
        """
        Caso in cui il prodotto specificato tramite la pk non esiste
        """
        prev_count = self.acquirente.prodotti.count()
        url = reverse("ordine", kwargs={"pk": self.prodotto.pk+1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)
        self.assertEqual(self.acquirente.prodotti.count(), prev_count)

    def test_ordine_utente_possiede_gia_il_prodotto(self):
        """
        Caso in cui l'utente possiede già il prodotto di cui vuole fare l'ordine
        """
        self.prodotto.acquirenti.add(self.acquirente)

        prev_count = self.acquirente.prodotti.count()
        url = reverse("ordine", kwargs={"pk": self.prodotto.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("pagina_negozio", kwargs={"pk": self.prodotto.pk}))
        self.assertEqual(self.acquirente.prodotti.count(), prev_count)

    def test_ordine_utente_accede_alla_pagina_con_metodo_get(self):
        """
        Caso in cui l'utente accede alla pagina del form dell'ordine con il metodo GET,
        quindi la prima volta, quando non ha ancora compilato il form
        """
        url = reverse("ordine", kwargs={"pk": self.prodotto.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertTemplateUsed(response, "prodotti/ordine.html")
        self.assertIsInstance(response.context["form"], OrdineForm)
        self.assertEqual(response.context["prodotto"], self.prodotto)
        self.assertNotIn(self.acquirente, self.prodotto.acquirenti.all())
        self.assertNotIn(self.prodotto, self.acquirente.prodotti.all())

    def test_ordine_utente_accede_alla_pagina_con_metodo_post(self):
        """
        Caso in cui l'utente accede alla pagina del form con il metodo POST,
        quindi la seconda volta, dopo aver compilato il form
        """
        url = reverse("ordine", kwargs={"pk": self.prodotto.pk})
        response = self.client.post(url, {"intestatario_carta": "Nome Cognome", "numero_carta": "1234567891234567", "scadenza_carta": "mmaaaa", "cvv": "123"})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("pagina_negozio", kwargs={"pk": self.prodotto.pk}))
        self.assertIn(self.acquirente, self.prodotto.acquirenti.all())
        self.assertIn(self.prodotto, self.acquirente.prodotti.all())

    def test_ordine_utente_compila_form_con_campi_non_validi(self):
        """
        Caso in cui l'utente compila il form con i campi non validi
        """
        url = reverse("ordine", kwargs={"pk": self.prodotto.pk})
        response = self.client.post(url, {"intestatario_carta": "Nome Cognome", "numero_carta": "1234567", "scadenza_carta": "mmaaa", "cvv": "13"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertTemplateUsed(response, "prodotti/ordine.html")
        self.assertIsInstance(response.context["form"], OrdineForm)
        self.assertEqual(response.context["prodotto"], self.prodotto)

        self.assertFalse(response.context["form"].is_valid())
        self.assertEqual(response.context["form"].errors["numero_carta"][0], "Ensure this value has at least 16 characters (it has 7).")
        self.assertEqual(response.context["form"].errors["scadenza_carta"][0], "Ensure this value has at least 6 characters (it has 5).")
        self.assertEqual(response.context["form"].errors["cvv"][0], "Ensure this value has at least 3 characters (it has 2).")

        self.assertNotIn(self.acquirente, self.prodotto.acquirenti.all())
        self.assertNotIn(self.prodotto, self.acquirente.prodotti.all())