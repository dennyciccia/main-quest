from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView
from MainQuest.forms import SearchForm
from prodotti.forms import OrdineForm, RecensioneForm, CreaDomandaForm, RispondiDomandaForm, ProdottoForm
from prodotti.models import Prodotto, Recensione, Domanda
from braces.views import GroupRequiredMixin
from MainQuest.views import group_required


# Create your views here.

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
    prodotto = get_object_or_404(Prodotto, pk=pk)
    acquirente = request.user.acquirente_profile

    # controllo se l'acquirente possiede già il prodotto
    if prodotto.acquirenti.filter(pk=acquirente.pk).exists():
        messages.error(request, "Hai già acquistato questo prodotto.")
        return redirect("pagina_negozio", pk=pk)

    if request.method == "POST":
        form = OrdineForm(request.POST)
        if form.is_valid():
            prodotto.acquirenti.add(acquirente)
            messages.success(request, message="Prodotto acquistato con successo.")
            return redirect("pagina_negozio", pk=pk)
    else:
        form = OrdineForm()

    return render(request, template_name="prodotti/ordine.html", context={"form": form, "prodotto": prodotto, "title": "Ordine di "+prodotto.titolo})


class CreaRecensione(GroupRequiredMixin, CreateView):
    group_required = ["Acquirenti"]
    login_url = reverse_lazy("login")
    model = Recensione
    form_class = RecensioneForm
    template_name = "prodotti/scrivi_recensione.html"

    def dispatch(self, request, *args, **kwargs):
        prodotto = get_object_or_404(Prodotto, pk=kwargs["pk"])
        acquirente = request.user.acquirente_profile

        # controllo che l'acquirente non possiede il prodotto
        if not prodotto.acquirenti.filter(pk=acquirente.pk).exists():
            messages.error(request, "Non hai acquistato questo prodotto.")
            return redirect("pagina_negozio", pk=prodotto.pk)

        # controllo che l'acquirente non abbia già scritto una recensione
        if prodotto.recensioni.filter(utente=acquirente).exists():
            messages.error(request, "Hai già scritto una recensione per questo prodotto.")
            return redirect("pagina_negozio", pk=prodotto.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.kwargs["pk"])
        context["title"] = "Scrivi recensione"
        return context

    def form_valid(self, form):
        form.instance.data_pubblicazione = timezone.now().date()
        form.instance.utente = self.request.user.acquirente_profile
        form.instance.prodotto = Prodotto.objects.get(pk=self.kwargs['pk'])
        response = super().form_valid(form)
        messages.success(self.request, message="Recensione pubblicata.")
        return response

    def get_success_url(self):
        return reverse("pagina_negozio", kwargs={"pk": self.kwargs["pk"]})


class ModificaRecensione(GroupRequiredMixin, UpdateView):
    group_required = ["Acquirenti"]
    login_url = reverse_lazy("login")
    model = Recensione
    form_class = RecensioneForm
    template_name = "prodotti/modifica_recensione.html"

    def dispatch(self, request, *args, **kwargs):
        recensione = get_object_or_404(Recensione, pk=kwargs["pk"])
        acquirente = request.user.acquirente_profile

        # controllo che l'acquirente abbia scritto la recensione
        if not recensione.utente == acquirente:
            messages.error(request, "Non hai scritto questa recensione.")
            return redirect("pagina_negozio", pk=recensione.prodotto.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.object.prodotto.pk)
        context["title"] = "Modifica recensione"
        return context

    def get_success_url(self):
        prodotto = self.get_context_data()["prodotto"]
        return reverse("pagina_negozio", kwargs={"pk": prodotto.pk})


@group_required("Acquirenti")
def elimina_recensione(request, pk):
    recensione = get_object_or_404(Recensione, pk=pk)
    prodotto = recensione.prodotto

    # controllo che l'utente abbia scritto la recensione
    if request.user.acquirente_profile != recensione.utente:
        messages.error(request, "Non hai scritto questa recensione.")
        return redirect("pagina_negozio", pk=prodotto.pk)

    recensione.delete()
    messages.success(request, message="Recensione eliminata.")

    return redirect(reverse("pagina_negozio", kwargs={"pk": prodotto.pk}))


class CreaDomanda(GroupRequiredMixin, CreateView):
    group_required = ["Acquirenti"]
    login_url = reverse_lazy("login")
    model = Domanda
    form_class = CreaDomandaForm
    template_name = "prodotti/fai_domanda.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.kwargs["pk"])
        context["title"] = "Fai una domanda"
        return context

    def form_valid(self, form):
        form.instance.utente = self.request.user.acquirente_profile
        form.instance.prodotto = Prodotto.objects.get(pk=self.kwargs['pk'])
        response = super().form_valid(form)
        messages.success(self.request, message="Domanda pubblicata.")
        return response

    def get_success_url(self):
        return reverse("pagina_negozio", kwargs={"pk": self.kwargs["pk"]})


class RispondiDomanda(GroupRequiredMixin, UpdateView):
    group_required = ["Acquirenti"]
    login_url = reverse_lazy("login")
    model = Domanda
    form_class = RispondiDomandaForm
    template_name = "prodotti/rispondi_domanda.html"

    def dispatch(self, request, *args, **kwargs):
        domanda = get_object_or_404(Domanda, pk=self.kwargs["pk"])
        prodotto = domanda.prodotto
        acquirente = request.user.acquirente_profile

        # controllo se l'acquirente possiede il prodotto
        if not prodotto.acquirenti.filter(pk=acquirente.pk).exists():
            messages.error(request, "Non hai acquistato questo prodotto.")
            return redirect("pagina_negozio", pk=prodotto.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prodotto"] = Prodotto.objects.get(pk=self.object.prodotto.pk)
        context["ttile"] = "Rispondi a una domanda"
        return context

    def form_valid(self, form):
        form.instance.utente_risposta = self.request.user.acquirente_profile
        response = super().form_valid(form)
        messages.success(self.request, message="Risposta pubblicata con successo.")
        return response

    def get_success_url(self):
        prodotto = self.get_context_data()["prodotto"]
        return reverse("pagina_negozio", kwargs={"pk": prodotto.pk})


class PubblicaProdotto(GroupRequiredMixin, CreateView):
    group_required = ["Venditori"]
    login_url = reverse_lazy("login")
    model = Prodotto
    form_class = ProdottoForm
    template_name = "prodotti/crea_prodotto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Pubblica prodotto"
        return context

    def form_valid(self, form):
        form.instance.data_rilascio = timezone.now().date()
        form.instance.venditore = self.request.user.venditore_profile
        response = super().form_valid(form)
        messages.success(self.request, message="Prodotto pubblicato.")
        return response

    def get_success_url(self):
        return reverse("pagina_negozio", kwargs={"pk": self.object.pk})


class ModificaProdotto(GroupRequiredMixin, UpdateView):
    group_required = ["Venditori"]
    login_url = reverse_lazy("login")
    model = Prodotto
    form_class = ProdottoForm
    template_name = "prodotti/modifica_prodotto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modifica prodotto"
        return context

    def dispatch(self, request, *args, **kwargs):
        prodotto = get_object_or_404(Prodotto, pk=self.kwargs["pk"])
        venditore = request.user.venditore_profile

        # controllo se il venditore è il proprietario del prodotto
        if prodotto.venditore != venditore:
            messages.error(request, "Non sei il proprietario di questo prodotto.")
            return redirect("pagina_negozio", pk=prodotto.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("pagina_negozio", kwargs={"pk": self.object.pk})


@group_required("Venditori")
def elimina_prodotto(request, pk):
    prodotto = get_object_or_404(Prodotto, pk=pk)
    venditore = request.user.venditore_profile

    # controllo se il venditore è il proprietario del prodotto
    if prodotto.venditore != venditore:
        messages.error(request, "Non sei il proprietario di questo prodotto.")
        return redirect("pagina_negozio", pk=prodotto.pk)

    prodotto.delete()
    messages.success(request, message="Prodotto eliminato.")
    return redirect("profilo_venditore", venditore.pk)