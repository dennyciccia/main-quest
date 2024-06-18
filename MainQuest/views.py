from datetime import timedelta
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.timezone import now
from MainQuest.forms import SearchForm
from prodotti.models import Prodotto
from utenti.models import Utente, Editore, Sviluppatore


def home(request):
    # ottengo le liste dei giochi più popolari e dei giochi più recenti
    primi_n = 3
    popolari = Prodotto.objects.annotate(num_acquirenti=Count('acquirenti')).order_by('-num_acquirenti')[:primi_n]
    recenti = Prodotto.objects.filter(data_rilascio__gte=(now() - timedelta(days=30)))

    #inizializzo il form
    form = SearchForm()

    # definisco il context
    context = {"title": "Home", "popolari": popolari, "recenti": recenti, "form": form}

    return render(request, template_name="home.html", context=context)

def login(request):
    pass

def register(request):
    pass

def risultati_ricerca(request):
    # istanzio il form con i valori inseriti dall'utente che ora sono nel POST
    form = SearchForm(request.POST)

    # se il form non ha errori
    if form.is_valid():
        search_terms = form.cleaned_data.get("search_terms")

        # ricerca dei risultati
        prodotti_results = Prodotto.objects.filter(titolo__icontains=search_terms)
        utenti_results = Utente.objects.filter(nome__icontains=search_terms)
        editori_results = Editore.objects.filter(nome__icontains=search_terms)
        sviluppatori_results = Sviluppatore.objects.filter(nome__icontains=search_terms)

        nessun_risultato = not prodotti_results.exists() and not utenti_results.exists() and not editori_results.exists() and not sviluppatori_results.exists()

        # creazione del context
        context = {"prodotti": prodotti_results, "utenti": utenti_results, "editori": editori_results, "sviluppatori": sviluppatori_results, "nessun_risultato": nessun_risultato}

        return render(request, template_name="risultati_ricerca.html", context=context)

    # se il form ha errori ritorna alla home
    return redirect("home")