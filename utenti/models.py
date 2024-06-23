from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    pass

class Acquirente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='acquirente_profile')
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField(upload_to="profile_pics/", default="media/imgs/default_profile_image.png")
    biografia = models.TextField(blank=True, default="")

    def type(self):
        return "acquirente"

    class Meta:
        verbose_name_plural = "Acquirenti"

class Venditore(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='venditore_profile')
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField(upload_to="profile_pics/", default="media/imgs/default_profile_image.png")

    def type(self):
        return "venditore"

    class Meta:
        verbose_name_plural = "Venditori"
