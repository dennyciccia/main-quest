from django.db import models
from utenti.models import Editore, Sviluppatore, Utente

# Create your models here.
class Prodotto(models.Model):
    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    prezzo = models.DecimalField(decimal_places=2, max_digits=10)
    requisiti = models.CharField(max_length=500)
    data_rilascio = models.DateField()
    editore = models.ForeignKey(Editore, on_delete=models.CASCADE, related_name="prodotti")
    sviluppatore = models.ForeignKey(Sviluppatore, null=True, on_delete=models.SET_NULL, related_name="prodotti")
    acquirenti = models.ManyToManyField(Utente, related_name="prodotti")

    class Meta:
        verbose_name_plural = "Prodotti"

class Immagine(models.Model):
    img = models.ImageField()
    testo_alternativo = models.CharField(max_length=100)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="immagini")

    class Meta:
        verbose_name_plural = "Immagini"

class Recensione(models.Model):
    testo = models.TextField(blank=True)
    voto = models.DecimalField(decimal_places=1, max_digits=10)
    data_pubblicazione = models.DateField()
    utente = models.ForeignKey(Utente, null=True, on_delete=models.SET_NULL, related_name="recensioni")
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="recensioni")

    class Meta:
        verbose_name_plural = "Recensioni"

class Domanda(models.Model):
    testo = models.CharField(max_length=500)
    risposta = models.CharField(max_length=500, blank=True)
    utente = models.ForeignKey(Utente, null=True, on_delete=models.SET_NULL, related_name="domande")
    utente_risposta = models.ForeignKey(Utente, null=True, on_delete=models.SET_NULL, related_name="risposte")
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="domande")

    class Meta:
        verbose_name_plural = "Domande"
