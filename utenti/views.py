from django.shortcuts import render
from django.views.generic import DetailView
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
        return context


class ProfiloVenditore(DetailView):
    model = Venditore
    template_name = "utenti/profilo_venditore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("next") is not None:
            context["next"] = self.request.GET["next"]
            context["terms"] = self.request.GET["terms"]
        return context

