"""
URL configuration for MainQuest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

urlpatterns = [
    path("game/<int:pk>", PaginaNegozio.as_view(), name="pagina_negozio"),
    path("game/pubblica/", PubblicaProdotto.as_view(), name="pubblica_prodotto"),
    path("game/modifica/<int:pk>", ModificaProdotto.as_view(), name="modifica_prodotto"),
    path("game/elimina/<int:pk>", elimina_prodotto, name="elimina_prodotto"),

    path("ordine/<int:pk>", ordine, name="ordine"),

    path("recensione/pubblica/<int:pk>", CreaRecensione.as_view(), name="scrivi_recensione"),
    path("recensione/modifica/<int:pk>", ModificaRecensione.as_view(), name="modifica_recensione"),
    path("recensione/elimina/<int:pk>", elimina_recensione, name="elimina_recensione"),

    path("domanda/chiedi/<int:pk>", CreaDomanda.as_view(), name="fai_domanda"),
    path("domanda/rispondi/<int:pk>", RispondiDomanda.as_view(), name="rispondi_domanda"),
]
