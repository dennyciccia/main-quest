from django.shortcuts import render
from django.views.generic.detail import DetailView
from utenti.models import Acquirente, Venditore


# Create your views here.

class ProfiloAcquirente(DetailView):
    model = Acquirente
    template_name = "utenti/profilo_acquirente.html"


class ProfiloVenditore(DetailView):
    model = Venditore
    template_name = "utenti/profilo_venditore.html"

