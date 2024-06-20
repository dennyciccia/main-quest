from django.shortcuts import render
from django.views.generic import DetailView

from prodotti.models import Prodotto


# Create your views here.

class PaginaNegozio(DetailView):
    model = Prodotto
    template_name = "prodotti/pagina_negozio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("next") is not None:
            context["next"] = self.request.GET["next"]
            context["terms"] = self.request.GET["terms"]
        return context