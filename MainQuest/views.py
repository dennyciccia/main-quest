from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm
from MainQuest.forms import SearchForm, RegisterForm
from prodotti.models import Prodotto
from utenti.models import Acquirente, Venditore
import django.contrib.auth as dj
from datetime import timedelta


def home(request):
    # ottengo le liste dei giochi più popolari e dei giochi più recenti
    primi_n = 3
    popolari = Prodotto.objects.annotate(num_acquirenti=Count('acquirenti')).order_by('-num_acquirenti')[:primi_n]
    recenti = Prodotto.objects.filter(data_rilascio__gte=(now() - timedelta(days=30)))

    #inizializzo il form per la ricerca
    form = SearchForm()

    # definisco il context
    context = {"title": "Home", "popolari": popolari, "recenti": recenti, "search_form": form}

    return render(request, template_name="home.html", context=context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            u = None
            if request.POST["user_type"] == "acquirente":
                g = Group.objects.get(name="Acquirenti")
                u = Acquirente()
                u.biografia = ""
            elif request.POST["user_type"] == "venditore":
                g = Group.objects.get(name="Venditori")
                u = Venditore()
            u.user = user
            u.nome = request.POST["username"]
            u.foto_profilo = "imgs/default_profile_image.png"
            u.save()
            messages.success(request, message="Registrazione avvenuta con successo!")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, template_name="register.html", context={"form": form, "next": request.GET.get("next")})

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
    next_url = request.GET.get("next", '')
    return render(request, template_name="login.html", context={"form": form, "next": next_url})

@login_required
def logout(request):
    dj.logout(request)
    return redirect("home")

def risultati_ricerca(request):
    def trova_risultati(st):
        # ricerca dei risultati
        prodotti_results = Prodotto.objects.filter(titolo__icontains=st)
        acquirenti_results = Acquirente.objects.filter(nome__icontains=st)
        venditori_results = Venditore.objects.filter(nome__icontains=st)
        nessun_risultato = not prodotti_results.exists() and not acquirenti_results.exists() and not venditori_results.exists()
        # creazione del context
        context = {"prodotti": prodotti_results, "acquirenti": acquirenti_results, "venditori": venditori_results, "nessun_risultato": nessun_risultato, "terms": search_terms}
        return context

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