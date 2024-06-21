from django import forms
from utenti.models import Acquirente


class ModificaProfiloAcquirenteForm(forms.ModelForm):
    # campi del form
    username = forms.CharField(label="Nome utente", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    clear_image = forms.BooleanField(label="Rimuovi foto profilo", required=False)
    foto_profilo = forms.ImageField(label="Foto profilo", widget=forms.FileInput, required=False)
    biografia = forms.CharField(label="Biografia", widget=forms.Textarea, required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label="Conferma password", widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Acquirente
        fields = ["username", "email", "password1", "password2", "clear_image", "foto_profilo", "biografia"]

    # valori iniziali dei campi del form
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ModificaProfiloAcquirenteForm, self).__init__(*args, **kwargs)
        self.fields["username"].initial = user.username
        self.fields["email"].initial = user.email
        self.fields["foto_profilo"].initial = user.acquirente_profile.foto_profilo
        self.fields["biografia"].initial = user.acquirente_profile.biografia

    # verifica che le due password corrispondano
    def clean(self):
        cleaned_data = super(ModificaProfiloAcquirenteForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 is not None and password1 != password2:
            self.add_error("password2", "Le password non corrispondono")

    # aggiorna le informazioni
    def save(self, commit=True):
        acquirente = super(ModificaProfiloAcquirenteForm, self).save(commit=False)

        user = acquirente.user
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        if self.cleaned_data["password1"]: user.set_password(self.cleaned_data["password1"])
        acquirente.nome = user.username
        if self.cleaned_data["clear_image"]: acquirente.foto_profilo = "imgs/default_profile_image.png"
        else: acquirente.foto_profilo = self.cleaned_data["foto_profilo"]
        acquirente.biografia = self.cleaned_data["biografia"]

        if commit:
            user.save()
            acquirente.save()
        return acquirente