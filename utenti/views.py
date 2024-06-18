from django.shortcuts import render
from django.views.generic.detail import DetailView
from utenti.models import Utente, Editore, Sviluppatore


# Create your views here.

class ProfiloAcquirente(DetailView):
    model = Utente
    template_name = "utenti/profilo_utente.html"

class ProfiloEditoreSviluppatore(DetailView):
    template_name = "utenti/profilo_editore_sviluppatore.html"

class ProfiloEditore(ProfiloEditoreSviluppatore):
    model = Editore

class ProfiloSviluppatore(ProfiloEditoreSviluppatore):
    model = Sviluppatore
