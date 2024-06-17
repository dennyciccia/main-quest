from django.shortcuts import render
from django.views.generic.detail import DetailView

from prodotti.models import Prodotto


# Create your views here.

def cerca():
    pass

class PaginaNegozio(DetailView):
    model = Prodotto
    template_name="prodotti/pagina_negozio.html"