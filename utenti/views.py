from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView
from MainQuest.forms import SearchForm
from utenti.forms import ModificaProfiloAcquirenteForm
from utenti.models import Acquirente, Venditore, CustomUser


# Create your views here.

class ProfiloAcquirente(DetailView):
    model = Acquirente
    template_name = "utenti/profilo_acquirente.html"

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


@login_required(login_url="login")
def modifica_profilo_acquirente(request, pk):
    user = request.user
    acquirente = request.user.acquirente_profile

    if request.method == "POST":
        form = ModificaProfiloAcquirenteForm(request.POST, request.FILES, user=user, instance=acquirente)
        if form.is_valid():
            form.save()
            # tiene l'utente loggato dopo il cambio di password
            update_session_auth_hash(request, user)
            return redirect("profilo_acquirente", pk=pk)
    else:
        form = ModificaProfiloAcquirenteForm(user=user)
    return render(request, template_name="utenti/modifica_profilo_acquirente.html", context={"form": form, "next": request.GET.get("next")})


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


@login_required(login_url="login")
def elimina_account(request, pk):
    if request.GET.get("commit"):
        # elimina
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        messages.success(request, message="Utente eliminato.")
        return redirect("home")

    # chiedi conferma eliminazione
    return render(request, template_name="utenti/conferma_eliminazione_account.html", context={"next": request.GET.get("next")})