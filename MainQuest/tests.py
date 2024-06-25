from django.test import TestCase
from django.utils import timezone
from MainQuest.views import trova_risultati
from prodotti.models import Prodotto
from utenti.models import Acquirente, Venditore, CustomUser


class TrovaRisultatiTest(TestCase):
    def setUp(self):
        self.account_acquirente = CustomUser.objects.create(username="Acquirente di test - 12", password="password")
        self.acquirente = Acquirente.objects.create(user=self.account_acquirente, nome=self.account_acquirente.username)
        self.account_venditore = CustomUser.objects.create(username="Venditore di test - 13", password="password")
        self.venditore = Venditore.objects.create(user=self.account_venditore, nome=self.account_venditore.username)
        self.prodotto = Prodotto.objects.create(titolo="Prodotto di test - 23", prezzo=19.99, data_rilascio=timezone.now().date(), venditore=self.venditore)

    def test_trova_risultati_prodotti_acquirenti_venditori(self):
        """
        Caso in cui ci sono risultati per Prodotti, Acquirenti e Venditori.
        """
        search_terms = "test"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),1)
        self.assertEqual(risultati["prodotti"].first(), self.prodotto)
        self.assertEqual(risultati["acquirenti"].count(),1)
        self.assertEqual(risultati["acquirenti"].first(), self.acquirente)
        self.assertEqual(risultati["venditori"].count(),1)
        self.assertEqual(risultati["venditori"].first(), self.venditore)
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_prodotti_acquirenti(self):
        """
        Caso in cui ci sono risultati per Prodotti e Acquirenti
        """
        search_terms = "2"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),1)
        self.assertEqual(risultati["prodotti"].first(), self.prodotto)
        self.assertEqual(risultati["acquirenti"].count(),1)
        self.assertEqual(risultati["acquirenti"].first(), self.acquirente)
        self.assertEqual(risultati["venditori"].count(),0)
        self.assertIsNone(risultati["venditori"].first())
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_prodotti_venditori(self):
        """
        Caso in cui ci sono risultati per Prodotti e Venditori
        """
        search_terms = "3"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),1)
        self.assertEqual(risultati["prodotti"].first(), self.prodotto)
        self.assertEqual(risultati["acquirenti"].count(),0)
        self.assertIsNone(risultati["acquirenti"].first())
        self.assertEqual(risultati["venditori"].count(),1)
        self.assertEqual(risultati["venditori"].first(), self.venditore)
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_acquirenti_venditori(self):
        """
        Caso in cui ci sono risultati per Acquirenti e Venditori
        """
        search_terms = "1"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),0)
        self.assertIsNone(risultati["prodotti"].first())
        self.assertEqual(risultati["acquirenti"].count(),1)
        self.assertEqual(risultati["acquirenti"].first(), self.acquirente)
        self.assertEqual(risultati["venditori"].count(),1)
        self.assertEqual(risultati["venditori"].first(), self.venditore)
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_prodotti(self):
        """
        Caso in cui ci sono risultati per Prodotti
        """
        search_terms = "prodotto"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),1)
        self.assertEqual(risultati["prodotti"].first(), self.prodotto)
        self.assertEqual(risultati["acquirenti"].count(),0)
        self.assertIsNone(risultati["acquirenti"].first())
        self.assertEqual(risultati["venditori"].count(),0)
        self.assertIsNone(risultati["venditori"].first())
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_acquirenti(self):
        """
        Caso in cui ci sono risultati per Acquirenti
        """
        search_terms = "acquirente"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),0)
        self.assertIsNone(risultati["prodotti"].first())
        self.assertEqual(risultati["acquirenti"].count(),1)
        self.assertEqual(risultati["acquirenti"].first(), self.acquirente)
        self.assertEqual(risultati["venditori"].count(),0)
        self.assertIsNone(risultati["venditori"].first())
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_venditori(self):
        """
        Caso in cui ci sono risultati per Venditori
        """
        search_terms = "venditore"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),0)
        self.assertIsNone(risultati["prodotti"].first())
        self.assertEqual(risultati["acquirenti"].count(),0)
        self.assertIsNone(risultati["acquirenti"].first())
        self.assertEqual(risultati["venditori"].count(),1)
        self.assertEqual(risultati["venditori"].first(), self.venditore)
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_nessun_risultato(self):
        """
        Caso in cui non ci sono risultati
        """
        search_terms = "vuoto"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(), 0)
        self.assertIsNone(risultati["prodotti"].first())
        self.assertEqual(risultati["acquirenti"].count(), 0)
        self.assertIsNone(risultati["acquirenti"].first())
        self.assertEqual(risultati["venditori"].count(), 0)
        self.assertIsNone(risultati["venditori"].first())
        self.assertTrue(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_nessun_search_term(self):
        """
        Caso in cui non vengono specificati search terms
        """
        search_terms = ""
        risultati = trova_risultati(search_terms)

        self.assertIsNone(risultati["prodotti"])
        self.assertIsNone(risultati["acquirenti"])
        self.assertIsNone(risultati["venditori"])
        self.assertTrue(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_search_terms_con_spazi_bianchi(self):
        """
        Caso in cui i search terms hanno spazi bianchi
        """
        search_terms = "prodotto di test"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),1)
        self.assertEqual(risultati["prodotti"].first(), self.prodotto)
        self.assertEqual(risultati["acquirenti"].count(),0)
        self.assertIsNone(risultati["acquirenti"].first())
        self.assertEqual(risultati["venditori"].count(),0)
        self.assertIsNone(risultati["venditori"].first())
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)

    def test_trova_risultati_multipli(self):
        """
        Caso in cui ci sono risultati multipli per Prodotti, Acquirenti e Venditori
        """
        account_acquirente2 = CustomUser.objects.create(username="Acquirente di test - 12 (doppio)", password="password")
        acquirente2 = Acquirente.objects.create(user=account_acquirente2, nome=self.account_acquirente.username)
        account_venditore2 = CustomUser.objects.create(username="Venditore di test - 13 (doppio)", password="password")
        venditore2 = Venditore.objects.create(user=account_venditore2, nome=self.account_venditore.username)
        prodotto2 = Prodotto.objects.create(titolo="Prodotto di test - 23 (doppio)", prezzo=19.99, data_rilascio=timezone.now().date(), venditore=self.venditore)

        search_terms = "test"
        risultati = trova_risultati(search_terms)

        self.assertEqual(risultati["prodotti"].count(),2)
        self.assertEqual(risultati["acquirenti"].count(),2)
        self.assertEqual(risultati["venditori"].count(),2)
        self.assertFalse(risultati["nessun_risultato"])
        self.assertEqual(risultati["terms"], search_terms)