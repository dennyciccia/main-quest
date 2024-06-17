from datetime import timedelta

from django.db.models import Count
from django.shortcuts import render
from django.utils.timezone import now

from prodotti.models import Prodotto


def home(request):
    # ottengo le liste dei giochi più popolari e dei giochi più recenti
    primi_n = 3
    popolari = Prodotto.objects.annotate(num_acquirenti=Count('acquirenti')).order_by('-num_acquirenti')[:primi_n]
    recenti = Prodotto.objects.filter(data_rilascio__gte=(now() - timedelta(days=30)))

    # definisco il context
    context = {"title": "Home", "popolari": popolari, "recenti": recenti}

    return render(request, template_name="home.html", context=context)

def login(request):
    pass

def register(request):
    pass