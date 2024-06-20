from django.shortcuts import render
from django.views.generic import DetailView

from MainQuest.forms import SearchForm
from utenti.models import Acquirente, Venditore


# Create your views here.

class ProfiloAcquirente(DetailView):
    model = Acquirente
    template_name = "utenti/profilo_acquirente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("next") is not None:
            context["next"] = self.request.GET["next"]
            context["terms"] = self.request.GET["terms"]
        # inizializzo il form per la ricerca
        form = SearchForm()
        context["search_form"] = form
        return context


class ProfiloVenditore(DetailView):
    model = Venditore
    template_name = "utenti/profilo_venditore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ottengo il next e i terms se provengo da una pagina che me li ha dati
        if self.request.GET.get("next") is not None:
            context["next"] = self.request.GET["next"]
            context["terms"] = self.request.GET["terms"]
        # inizializzo il form per la ricerca
        form = SearchForm()
        context["search_form"] = form
        return context

