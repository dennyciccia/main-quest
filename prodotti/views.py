from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView
from MainQuest.forms import SearchForm
from prodotti.forms import OrdineForm, RecensioneForm, CreaDomandaForm, RispondiDomandaForm
from prodotti.models import Prodotto, Recensione, Domanda
from utenti.models import Acquirente
from braces.views import GroupRequiredMixin, LoginRequiredMixin


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
        # controlla se l'utente può scrivere la recensione
        flag = False
        if hasattr(self.request.user, "acquirente_profile"):
            for r in self.object.recensioni.all():
                if self.request.user.acquirente_profile == r.utente:
                    flag = True
        context["user_ha_scritto_recensione"] = flag
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


class CreaRecensione(GroupRequiredMixin, CreateView):
    group_required = ["Acquirenti"]
    model = Recensione
    form_class = RecensioneForm
    template_name = "prodotti/scrivi_recensione.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.data_pubblicazione = timezone.now().date()
        form.instance.utente = self.request.user.acquirente_profile
        form.instance.prodotto = Prodotto.objects.get(pk=self.kwargs['pk'])
        response = super().form_valid(form)
        messages.success(self.request, message="Recensione pubblicata.")
        return response

    def get_success_url(self):
        return reverse_lazy("pagina_negozio", kwargs={"pk": self.kwargs["pk"]})


class ModificaRecensione(GroupRequiredMixin, UpdateView):
    group_required = ["Acquirenti"]
    model = Recensione
    form_class = RecensioneForm
    template_name = "prodotti/modifica_recensione.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.object.prodotto.pk)
        return context

    def get_success_url(self):
        prodotto = self.get_context_data()["prodotto"]
        return reverse_lazy("pagina_negozio", kwargs={"pk": prodotto.pk})


@login_required(login_url="login")
def elimina_recensione(request, pk):
    recensione = Recensione.objects.get(pk=pk)
    prodotto = recensione.prodotto
    recensione.delete()
    messages.success(request, message="Recensione eliminata.")
    return redirect(reverse("pagina_negozio", kwargs={"pk": prodotto.pk}))


class CreaDomanda(GroupRequiredMixin, CreateView):
    group_required = ["Acquirenti"]
    model = Domanda
    form_class = CreaDomandaForm
    template_name = "prodotti/fai_domanda.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.utente = self.request.user.acquirente_profile
        form.instance.prodotto = Prodotto.objects.get(pk=self.kwargs['pk'])
        response = super().form_valid(form)
        messages.success(self.request, message="Domanda pubblicata.")
        return response

    def get_success_url(self):
        return reverse_lazy("pagina_negozio", kwargs={"pk": self.kwargs["pk"]})

class RispondiDomanda(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = Domanda
    form_class = RispondiDomandaForm
    template_name = "prodotti/rispondi_domanda.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.object.prodotto.pk)
        return context

    def form_valid(self, form):
        if hasattr(self.request.user, "acquirente_profile"):
            utente_risposta = self.request.user.acquirente_profile
        elif hasattr(self.request.user, "venditore_profile"):
            utente_risposta = self.request.user.venditore_profile
        form.instance.utente_risposta = utente_risposta
        response = super().form_valid(form)
        messages.success(self.request, message="Risposta pubblicata.")
        return response

    def get_success_url(self):
        prodotto = self.get_context_data()["prodotto"]
        return reverse_lazy("pagina_negozio", kwargs={"pk": prodotto.pk})