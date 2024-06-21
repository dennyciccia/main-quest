from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from MainQuest.forms import SearchForm
from prodotti.forms import OrdineForm
from prodotti.models import Prodotto
from utenti.models import Acquirente


# Create your views here.

def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group, login_url="login")


class PaginaNegozio(DetailView):
    model = Prodotto
    template_name = "prodotti/pagina_negozio.html"

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

@group_required("Acquirenti")
def ordine(request, pk):
    prodotto = Prodotto.objects.get(pk=pk)
    if request.method == "POST":
        form = OrdineForm(request.POST)
        if form.is_valid():
            acquirente = Acquirente.objects.get(pk=request.user.acquirente_profile.pk)
            prodotto.acquirenti.add(acquirente)
            messages.success(request, message="Prodotto acquistato con successo.")
            return redirect("pagina_negozio", pk=pk)
    else:
        form = OrdineForm()
    return render(request, template_name="prodotti/ordine.html", context={"form": form, "prodotto": prodotto})