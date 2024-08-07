from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from prodotti.models import Recensione, Domanda, Prodotto


class OrdineForm(forms.Form):
    intestatario_carta = forms.CharField(label="Intestatario carta", max_length=100)
    numero_carta = forms.CharField(label="Numero carta", min_length=16, max_length=16)
    scadenza_carta = forms.CharField(label="Scadenza carta", min_length=6, max_length=6)
    cvv = forms.CharField(label="CVV", min_length=3, max_length=3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["numero_carta"].validators.append(MinLengthValidator(16))
        self.fields["numero_carta"].validators.append(MaxLengthValidator(16))
        self.fields["scadenza_carta"].validators.append(MinLengthValidator(6))
        self.fields["scadenza_carta"].validators.append(MaxLengthValidator(6))
        self.fields["cvv"].validators.append(MinLengthValidator(3))
        self.fields["cvv"].validators.append(MaxLengthValidator(3))


class RecensioneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["voto"].validators.append(MinValueValidator(1))
        self.fields["voto"].validators.append(MaxValueValidator(10))

    class Meta:
        model = Recensione
        fields = ("voto", "testo")


class CreaDomandaForm(forms.ModelForm):
    class Meta:
        model = Domanda
        fields = ("testo",)


class RispondiDomandaForm(forms.ModelForm):
    class Meta:
        model = Domanda
        fields = ("risposta",)

class ProdottoForm(forms.ModelForm):
    clear_image = forms.BooleanField(label="Rimuovi immagine", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["prezzo"].validators.append(MinValueValidator(0))

    def clean(self):
        cleaned_data = super(ProdottoForm, self).clean()
        if Prodotto.objects.filter(titolo__iexact=cleaned_data.get("titolo")).exclude(pk=self.instance.pk).exists():
            self.add_error("titolo", "Esiste già un prodotto con questo titolo")

    def save(self, commit=True):
        prodotto = super(ProdottoForm, self).save(commit=False)
        if self.cleaned_data["clear_image"]: prodotto.immagine = "imgs/placeholder_image.png"
        else: prodotto.immagine = self.cleaned_data["immagine"]
        if commit: prodotto.save()
        return prodotto

    class Meta:
        model = Prodotto
        fields = ("titolo", "descrizione", "genere", "prezzo", "requisiti", "immagine")