from django import forms
from django.contrib.auth.forms import UserCreationForm

from utenti.models import Acquirente, Venditore, CustomUser


class ModificaProfiloForm(forms.ModelForm):
    # campi del form
    username = forms.CharField(label="Nome utente", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    clear_image = forms.BooleanField(label="Rimuovi foto profilo", required=False)
    foto_profilo = forms.ImageField(label="Foto profilo", widget=forms.FileInput, required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label="Conferma password", widget=forms.PasswordInput(), required=False)

    # valori iniziali dei campi del form
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ModificaProfiloForm, self).__init__(*args, **kwargs)
        self.fields["username"].initial = user.username
        self.fields["email"].initial = user.email
        if hasattr(user, "acquirente_profile"): self.fields["foto_profilo"].initial = user.acquirente_profile.foto_profilo
        elif hasattr(user, "venditore_profile"): self.fields["foto_profilo"].initial = user.venditore_profile.foto_profilo


    # verifica che le due password corrispondano e che l'username sia disponibile
    def clean(self):
        cleaned_data = super(ModificaProfiloForm, self).clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Le password non corrispondono")

        if CustomUser.objects.filter(username__iexact=cleaned_data.get("username")).exclude(pk=self.instance.user.pk).exists():
            self.add_error("username", "Nome utente non disponibile")

    # aggiorna le informazioni
    def save(self, commit=True):
        utente = super(ModificaProfiloForm, self).save(commit=False)

        user = utente.user
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        utente.nome = user.username
        if self.cleaned_data["clear_image"]:
            utente.foto_profilo = "imgs/default_profile_image.png"
        else:
            utente.foto_profilo = self.cleaned_data["foto_profilo"]
        if hasattr(utente, "biografia"):
            utente.biografia = self.cleaned_data["biografia"]

        if commit:
            user.save()
            utente.save()
        return utente


class ModificaProfiloAcquirenteForm(ModificaProfiloForm):
    biografia = forms.CharField(label="Biografia", widget=forms.Textarea, required=False)

    class Meta:
        model = Acquirente
        fields = ["username", "email", "password1", "password2", "clear_image", "foto_profilo", "biografia"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(user=user, *args, **kwargs)
        self.fields["biografia"].initial = user.acquirente_profile.biografia


class ModificaProfiloVenditoreForm(ModificaProfiloForm):
    class Meta:
        model = Venditore
        fields = ["username", "email", "password1", "password2", "clear_image", "foto_profilo"]


class CreaModeratoreForm(UserCreationForm):
    username = forms.CharField(label="Nome moderatore", max_length=100)
    email = forms.EmailField(label="E-mail", max_length=100)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]