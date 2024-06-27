import pandas as pd
import numpy as np
from decimal import Decimal
from prodotti.models import Prodotto, Recensione
from utenti.models import Acquirente


def cosine_similarity(user1, user2):
    dot_product = np.dot(user1, user2)
    norm_user1 = Decimal(np.linalg.norm(user1))
    norm_user2 = Decimal(np.linalg.norm(user2))
    norm_product = norm_user1 * norm_user2
    if norm_product.is_zero(): return Decimal(0)
    return dot_product / norm_product


def recommendations(current_user, top_n=None, threshold=None):
    if top_n is None and threshold is None or top_n is not None and threshold is not None:
        raise ValueError("Specifica top_n o threshold ma non entrambi")

    utenti = Acquirente.objects.all()
    prodotti = Prodotto.objects.all()
    recensioni = Recensione.objects.all()

    # inizializzazione matrice
    user_item_matrix = pd.DataFrame(index=[u.pk for u in utenti], columns=[p.pk for p in prodotti], data=Decimal(0))

    # popolazione matrice
    for utente in utenti:
        for prodotto in utente.prodotti.all():
            user_item_matrix.at[utente.pk, prodotto.pk] = Decimal(6) # punteggio 6 solo per aver acquistato

            recensione = recensioni.filter(utente=utente, prodotto=prodotto).first()
            if recensione:
                user_item_matrix.at[utente.pk, prodotto.pk] = Decimal(recensione.voto) # se è stato dato un voto diventa il punteggio

    # calcolo delle similarità tra l'utente corrente e gli altri utenti
    similarity = dict()
    for utente in utenti:
        if utente != current_user:
            similarity[str(utente.pk)] = cosine_similarity(user_item_matrix.loc[current_user.pk].to_numpy(), user_item_matrix.loc[utente.pk].to_numpy())

    # calcolo del voto che l'utente potrebbe dare a ogni prodotto, escludendo quelli già acquistati
    prediction = dict()
    for prodotto in prodotti:
        if prodotto not in current_user.prodotti.all():
            somma = 0
            for utente in utenti:
                if utente != current_user:
                    somma += similarity[str(utente.pk)] * user_item_matrix.at[utente.pk, prodotto.pk]
            prediction[str(prodotto.pk)] = somma

    # selezione dei risultati
    prediction_sorted = dict(sorted(prediction.items(), key=lambda item: item[1], reverse=True))
    prodotti_consigliati = list()
    lista_pk_prodotti = list()

    if top_n is not None:
        lista_pk_prodotti = list(prediction_sorted.keys())[:top_n]
    if threshold is not None:
        lista_pk_prodotti = [ key for key, value in prediction_sorted if value >= threshold ]

    for pk in lista_pk_prodotti:
        prodotti_consigliati.append(Prodotto.objects.get(pk=pk))

    return prodotti_consigliati