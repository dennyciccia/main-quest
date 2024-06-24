from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from MainQuest.forms import SearchForm
from utenti.forms import ModificaProfiloAcquirenteForm, ModificaProfiloVenditoreForm
from utenti.models import Acquirente, Venditore, CustomUser
from MainQuest.views import group_required


# Create your views here.

class Profilo(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ottengo il next e i terms se provengo da una pagina che me li ha dati
        if self.request.GET.get("next") is not None:
            context["next"] = self.request.GET["next"]
            context["terms"] = self.request.GET["terms"]
        # inizializzo il form per la ricerca
        form = SearchForm()
        context["search_form"] = form
        # passo l'id dell'utente
        context["user_id"] = self.object.pk
        return context


class ProfiloAcquirente(Profilo):
    model = Acquirente
    template_name = "utenti/profilo_acquirente.html"


@group_required("Acquirenti")
def modifica_profilo_acquirente(request, pk):
    user = request.user
    acquirente = user.acquirente_profile
    oggetto_acquirente = get_object_or_404(Acquirente, pk=pk)

    # controllo se l'acquirente è il proprietario del profilo
    if oggetto_acquirente != acquirente:
        messages.error(request, "Puoi modificare solo il tuo profilo.")
        return redirect("profilo_acquirente", pk=acquirente.pk)

    if request.method == "POST":
        form = ModificaProfiloAcquirenteForm(request.POST, request.FILES, user=user, instance=acquirente)
        if form.is_valid():
            form.save()
            # tiene l'utente loggato dopo il cambio di password
            update_session_auth_hash(request, user)
            return redirect("profilo_acquirente", pk=pk)
    else:
        form = ModificaProfiloAcquirenteForm(user=user)

    return render(request, template_name="utenti/modifica_profilo_acquirente.html", context={"form": form, "user_id": pk})


class ProfiloVenditore(Profilo):
    model = Venditore
    template_name = "utenti/profilo_venditore.html"


@group_required("Venditori")
def modifica_profilo_venditore(request, pk):
    user = request.user
    venditore = user.venditore_profile
    oggetto_venditore = get_object_or_404(Venditore, pk=pk)

    # controllo se l'acquirente è il proprietario del profilo
    if oggetto_venditore != venditore:
        messages.error(request, "Puoi modificare solo il tuo profilo.")
        return redirect("profilo_venditore", pk=venditore.pk)

    if request.method == "POST":
        form = ModificaProfiloVenditoreForm(request.POST, request.FILES, user=user, instance=venditore)
        if form.is_valid():
            form.save()
            # tiene l'utente loggato dopo il cambio di password
            update_session_auth_hash(request, user)
            return redirect("profilo_venditore", pk=pk)
    else:
        form = ModificaProfiloVenditoreForm(user=user)
    return render(request, template_name="utenti/modifica_profilo_venditore.html", context={"form": form, "user_id": pk})


@login_required(login_url=reverse_lazy("login"))
def elimina_account(request, pk):
    utente = request.user
    account = get_object_or_404(CustomUser, pk=pk)

    # controllo che l'utente sia il proprietario dell'account
    if account != utente:
        messages.error(request, "Puoi eliminare solo il tuo account.")
        if hasattr(utente, "acquirente_profile"):
            return redirect("profilo_acquirente", pk=utente.pk)
        elif hasattr(utente, "venditore_profile"):
            return redirect("profilo_venditore", pk=utente.pk)
        else:
            return redirect("home")

    if request.GET.get("commit"):
        # elimina
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        messages.success(request, message="Account eliminato.")
        return redirect("home")

    # chiedi conferma eliminazione
    return render(request, template_name="utenti/conferma_eliminazione_account.html", context={"next": request.GET.get("next")})