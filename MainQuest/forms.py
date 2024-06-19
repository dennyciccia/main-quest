from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from prodotti.models import *
from utenti.models import *

class SearchForm(forms.Form):
    search_terms = forms.CharField(label="Cerca", max_length=100)

class RegisterForm(UserCreationForm):
    user_type= forms.ChoiceField(
        choices=[('acquirente', 'Acquirente'), ('venditore', 'Venditore')],
        widget=forms.RadioSelect,
        label='Registrati come'
    )
    username = forms.CharField(label="Nome utente", max_length=100)
    email = forms.EmailField(label="E-mail", max_length=100)
    #password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = CustomUser
        fields = ("user_type", "username", "email", "password1", "password2")

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome utente: ", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Password: ")
