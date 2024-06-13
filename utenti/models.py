from abc import ABC
from django.db import models
from prodotti.models import Prodotto

# Create your models here.
class Utente(models.Model):
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField()
    biografia = models.TextField()
    prodotti = models.ManyToManyField(Prodotto, related_name="acquirenti")

class Editore(models.Model):
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField()

class Sviluppatore(models.Model):
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField()
