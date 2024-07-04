from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm
from MainQuest.forms import SearchForm, RegisterForm
from prodotti.models import Prodotto, Recensione, Domanda
from utenti.models import Acquirente, Venditore
import django.contrib.auth as dj
from datetime import timedelta
from MainQuest.recommendation import recommendations


def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()

    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not in_group(request.user):
                messages.error(request, "Per accedere a questa pagina devi essere nel gruppo " + group_name)
                return redirect("login")
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
    #return user_passes_test(in_group, login_url=reverse_lazy("login"))


def trova_risultati(search_terms):
    # se non vengono specificati search terms non si ottiene nessun risultato
    if search_terms == "":
        return {"prodotti": None, "acquirenti": None, "venditori": None, "nessun_risultato": True, "terms": search_terms}

    # ricerca dei risultati
    prodotti_results = Prodotto.objects.filter(titolo__icontains=search_terms)
    acquirenti_results = Acquirente.objects.filter(nome__icontains=search_terms)
    venditori_results = Venditore.objects.filter(nome__icontains=search_terms)
    nessun_risultato = not prodotti_results.exists() and not acquirenti_results.exists() and not venditori_results.exists()
    # creazione del context
    context = {"prodotti": prodotti_results, "acquirenti": acquirenti_results, "venditori": venditori_results, "nessun_risultato": nessun_risultato, "terms": search_terms}
    return context


def home(request):
    # ottengo le liste dei giochi più popolari e dei giochi più recenti
    primi_n = 9
    popolari = Prodotto.objects.annotate(num_acquirenti=Count('acquirenti')).order_by('-num_acquirenti')[:primi_n]
    recenti = Prodotto.objects.filter(data_rilascio__gte=(now() - timedelta(days=30)))
    recenti = sorted(recenti, key=lambda x: x.data_rilascio, reverse=True)

    # inizializzo il form per la ricerca
    form = SearchForm()

    # determinazione dei prodotti consigliati con il recommendation system
    consigliati = None
    if hasattr(request.user, "acquirente_profile"):
        consigliati = recommendations(request.user.acquirente_profile, top_n=9)

    # definisco il context
    context = {"title": "Home - MainQuest", "popolari": popolari, "recenti": recenti, "search_form": form, "consigliati": consigliati}

    return render(request, template_name="home.html", context=context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            u = g = None
            if request.POST["user_type"] == "acquirente":
                g = Group.objects.get(name="Acquirenti")
                u = Acquirente()
                u.biografia = ""
            elif request.POST["user_type"] == "venditore":
                g = Group.objects.get(name="Venditori")
                u = Venditore()
            g.user_set.add(user)
            u.user = user
            u.pk = user.pk
            u.nome = request.POST["username"]
            u.foto_profilo = "imgs/default_profile_image.png"
            u.save()
            messages.success(request, message="Registrazione avvenuta con successo.")
            return redirect(reverse("login") + "?next=" + request.GET.get("next"))
    else:
        form = RegisterForm()
    next_url = request.GET.get("next") if request.GET.get("next") != reverse("logout") else '/'
    return render(request, template_name="register.html", context={"form": form, "next": next_url, "title": "Registrati"})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj.login(request, user)
            next_url = request.POST.get("next", "home")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    next_url = request.GET.get("next", '/') if request.GET.get("next", '/') != reverse("logout") else '/'
    return render(request, template_name="login.html", context={"form": form, "next": next_url, "title": "Login"})

@login_required(login_url=reverse_lazy("login"))
def logout(request):
    dj.logout(request)
    return render(request, template_name="logout.html", context={"title": "Logout"})

def risultati_ricerca(request):
    if request.method == "POST":
        # istanzio il form con i valori inseriti dall'utente che ora sono nel POST
        form = SearchForm(request.POST)
        # se il form non ha errori
        if form.is_valid():
            search_terms = form.cleaned_data.get("search_terms")
            # ricerca dei risultati
            context = trova_risultati(search_terms)
            return render(request, template_name="risultati_ricerca.html", context=context)
        # se il form ha errori ritorna alla home
        return redirect("home")

    elif request.method == "GET" and request.GET.get("terms") is not None:
        search_terms = request.GET.get("terms")
        # ricerca dei risultati
        context = trova_risultati(search_terms)
        return render(request, template_name="risultati_ricerca.html", context=context)

    else:
        return HttpResponseNotFound("Errore 404: Qualcosa è andato storto...")


@group_required("Moderatori")
def oscura_elemento(request, pk):
    classe = request.GET.get("classe")
    next = request.GET.get("next")
    if classe is None or next is None:
        return HttpResponseNotFound("Errore 404: Qualcosa è andato storto...")

    # se la classe specificata è uno tra i models
    if classe in ["Prodotto", "Recensione", "Domanda", "Acquirente", "Venditore"]:
        # controlla che l'elemento esiste e che non sia già stato oscurato
        elemento = get_object_or_404(eval(classe), pk=pk)
        if elemento.oscurato:
            messages.error(request, "Elemento già oscurato")
            return redirect(next)
        # oscura elemento
        elemento.oscurato = True
        elemento.save()
        messages.success(request, "Elemento oscurato")
        return redirect(next)
    else:
        return HttpResponseNotFound("Errore 404: Qualcosa è andato storto...")

@group_required("Moderatori")
def rendi_visibile_elemento(request, pk):
    classe = request.GET.get("classe")
    next = request.GET.get("next")
    if classe is None or next is None:
        return HttpResponseNotFound("Errore 404: Qualcosa è andato storto...")

    # se la classe specificata è uno tra i models
    if classe in ["Prodotto", "Recensione", "Domanda", "Acquirente", "Venditore"]:
        # controlla che l'elemento esiste e che sia già stato oscurato
        elemento = get_object_or_404(eval(classe), pk=pk)
        if not elemento.oscurato:
            messages.error(request, "Elemento non oscurato")
            return redirect(next)
        # oscura elemento
        elemento.oscurato = False
        elemento.save()
        messages.success(request, "Elemento reso di nuovo visibile")
        return redirect(next)
    else:
        return HttpResponseNotFound("Errore 404: Qualcosa è andato storto...")


@group_required("Moderatori")
def elementi_oscurati(request):
    form = SearchForm()

    prodotti = Prodotto.objects.filter(oscurato=True)
    recensioni = Recensione.objects.filter(oscurato=True)
    domande = Domanda.objects.filter(oscurato=True)
    acquirenti = Acquirente.objects.filter(oscurato=True)
    venditori = Venditore.objects.filter(oscurato=True)

    context = {"search_form": form, "prodotti": prodotti, "recensioni": recensioni, "domande": domande, "acquirenti": acquirenti, "venditori": venditori}

    return render(request, template_name="elementi_oscurati.html", context=context)