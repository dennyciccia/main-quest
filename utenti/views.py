from django.shortcuts import render
from django.views.generic.detail import DetailView
from utenti.models import Utente, Editore, Sviluppatore


# Create your views here.

class ProfiloAcquirente(DetailView):
    model = Utente
    template_name = "utenti/profilo_utente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back"] = self.request.META.get("HTTP_REFERER")

class ProfiloEditoreSviluppatore(DetailView):
    template_name = "utenti/profilo_editore_sviluppatore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back"] = self.request.META.get("HTTP_REFERER")
        return context

class ProfiloEditore(ProfiloEditoreSviluppatore):
    model = Editore

class ProfiloSviluppatore(ProfiloEditoreSviluppatore):
    model = Sviluppatore
