from django.db import models

# Create your models here.
class Utente(models.Model):
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField()
    biografia = models.TextField()

    class Meta:
        verbose_name_plural = "Utenti"

class Editore(models.Model):
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField()

    class Meta:
        verbose_name_plural = "Editori"

class Sviluppatore(models.Model):
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField()

    class Meta:
        verbose_name_plural = "Sviluppatori"