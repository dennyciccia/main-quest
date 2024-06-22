from datetime import date
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from prodotti.models import Recensione


class OrdineForm(forms.Form):
    intestatario_carta = forms.CharField(label="Intestatario carta", max_length=100)
    numero_carta = forms.CharField(label="Numero carta", min_length=16, max_length=16)
    scadenza_carta = forms.CharField(label="Scadenza carta", min_length=6, max_length=6)
    cvv = forms.CharField(label="CVV", min_length=3, max_length=3)


class CreaRecensioneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["voto"].validators.append(MinValueValidator(0))
        self.fields["voto"].validators.append(MaxValueValidator(10))

    class Meta:
        model = Recensione
        fields = ("voto", "testo")