from django.db import models
from utenti.models import Editore, Sviluppatore, Utente

# Create your models here.
class Prodotto(models.Model):
    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    prezzo = models.DecimalField(decimal_places=2)
    requisiti = models.CharField(max_length=500)
    data_rilascio = models.DateField()
    publisher = models.ForeignKey(Editore, on_delete=models.CASCADE, related_name="prodotti")
    developer = models.ForeignKey(Sviluppatore, on_delete=models.SET_NULL, related_name="prodotti")

class Recensione(models.Model):
    testo = models.TextField(blank=True)
    voto = models.DecimalField(decimal_places=1)
    data_pubblicazione = models.DateField()
    utente = models.ForeignKey(Utente, on_delete=models.SET_NULL, related_name="recensioni")
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="recensioni")

class Domanda(models.Model):
    testo = models.CharField(max_length=500)
    risposta = models.CharField(max_length=500, null=True)
    utente = models.ForeignKey(Utente, on_delete=models.SET_NULL, related_name="domande")
    utente_risposta = models.ForeignKey(Utente, on_delete=models.SET_NULL, related_name="risposte")
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="domande")

class Immagine(models.Model):
    img = models.ImageField()
    testo_alternativo = models.CharField(max_length=100)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="immagini")