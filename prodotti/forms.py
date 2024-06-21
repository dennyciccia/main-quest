from django import forms


class OrdineForm(forms.Form):
    intestatario_carta = forms.CharField(label="Intestatario carta", max_length=100)
    numero_carta = forms.CharField(label="Numero carta", min_length=16, max_length=16)
    scadenza_carta = forms.CharField(label="Scadenza carta", min_length=6, max_length=6)
    cvv = forms.CharField(label="CVV", min_length=3, max_length=3)