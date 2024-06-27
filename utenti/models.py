from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'

class CustomUser(AbstractUser):
    username_validator = MyValidator()
    username = models.CharField(
        _('username'),
        max_length=100,
        unique=True,
        help_text=_('Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
            error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

class Acquirente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='acquirente_profile')
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField(upload_to="profile_pics/", default="imgs/default_profile_image.png")
    biografia = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.nome} ({self.pk})"

    class Meta:
        verbose_name_plural = "Acquirenti"

class Venditore(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='venditore_profile')
    nome = models.CharField(max_length=100)
    foto_profilo = models.ImageField(upload_to="profile_pics/", default="media/imgs/default_profile_image.png")

    def __str__(self):
        return f"{self.nome} ({self.pk})"

    class Meta:
        verbose_name_plural = "Venditori"
