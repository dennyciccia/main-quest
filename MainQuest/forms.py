from django import forms
from prodotti.models import *
from utenti.models import *

class SearchForm(forms.Form):
    search_terms = forms.CharField(label='Cerca', max_length=100)
