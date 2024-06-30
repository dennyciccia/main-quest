from django.contrib.auth.models import Group

from prodotti.models import Prodotto, Recensione, Domanda
from utenti.models import CustomUser, Acquirente, Venditore
from datetime import date
from django.contrib.auth.hashers import make_password

def erase_db():
    print("Cancellazione DB ...")
    CustomUser.objects.all().delete()
    Acquirente.objects.all().delete()
    Venditore.objects.all().delete()
    Prodotto.objects.all().delete()
    Recensione.objects.all().delete()
    Domanda.objects.all().delete()
    #il resto si cancella in automatico

def init_db():
    if len(Prodotto.objects.all()) != 0:
        return

    print("Inizializzazione DB ...")

    # definizioni dati
    acquirentidict = {
        "nomi": ["Abstract Lettuce", "IronMaidenEnjoyer", "Ayaya", "Ritroder", "1TacticalBadger"],
        "foto": ["imgs/default_profile_image.png"]*5,
        "biografie": ["Mi piacciono i giochi sandbox", "Adoro la musica metal", "", "Skyrim lover", ""]
    }

    venditoridict = {
        "nomi": ["Bethesda Softworks", "CD PROJECT RED", "Bandai Namco Entertainment", "Xbox Game Studios", "Activision"],
        "foto": ["imgs/default_profile_image.png"]*5
    }

    prodottidict = {
        "titoli": ["The Elder Scrolls V: Skyrim Special Edition", "The Witcher 3: Wild Hunt", "Dark Souls: Remastered", "Minecraft", "Crash Bandicoot N. Sane Trilogy", "Dummy Game"],
        "descrizioni": ["Vincitore di oltre 200 premi Gioco dell’Anno, The Elder Scrolls V: Skyrim Special Edition porta sui vostri schermi il fantasy epico con dettagli mozzafiato. La Special Edition include l’acclamato gioco e gli add-on con nuove funzioni.",
                        "Vesti i panni di Geralt di Rivia, cacciatore di mostri, in una terra devastata dalla guerra e infestata da terribili creature. Il tuo contratto? Rintracciare Ciri, la Figlia della Profezia, un'arma vivente che può alterare il destino del mondo.",
                        "E poi venne il Fuoco. Rivivi l'esperienza che ha rivoluzionato il mondo dei videogiochi e dato vita a un nuovo genere. Esplora la terra di Lordran in una splendida versione rimasterizzata in altissima definizione a 60 fps.",
                        "Esplora mondi unici, sopravvivi alla notte e crea tutto quello che riesci a immaginare!",
                        "Crash Bandicoot™, il tuo marsupiale preferito, è tornato! Più bello e scatenato che mai, è pronto a lanciarsi nelle danze nella collezione Trilogia N. Sane.",
                        "Un gioco molto bello, talmente bello che sembra finto."],
        "prezzi": [39.99, 29.99, 39.99, 19.99, 39.99, 9.99],
        "requisiti": ["GeForce GTX 780 / Radeon R9 290", "GeForce GTX 1070 / Radeon RX 480", "GeForce GTX 660 / Radeon HD 7870", "GeForce GTX 700 / Radeon RX 200", "GeForce GTX 660 / Radeon HD 7850", "GeForce RTX 4090 / Radeon RX 7900 XTX"],
        "date_rilascio": [date(2016, 10, 28), date(2015, 5, 18), date(2018, 5, 24), date(2011, 11, 18), date(2018, 6, 29), date(2024, 6, 15)],
        "generi": ["RPG", "RPG", "Action RPG", "SandBox", "Platform 3D", "Open World"],
        "venditori": ["Bethesda Softworks", "CD PROJECT RED", "Bandai Namco Entertainment", "Xbox Game Studios", "Activision", "Bethesda Softworks"],
        "acquirenti": [["Ritroder", "1TacticalBadger"], ["IronMaidenLover, Ritroader"], [], ["Abstract Lettuce", "IronMaidenEnjoyer", "Ritroder", "1TacticalBadger"], ["Ritroder"], []]
    }

    immaginidict = {
        "imgs": ["imgs/placeholder_image.png"]*5,
        "testi_alternativi": ["immagine di gioco"]*5,
        "prodotti": ["The Elder Scrolls V: Skyrim Special Edition", "The Elder Scrolls V: Skyrim Special Edition", "Dark Souls: Remastered", "Minecraft", "Crash Bandicoot N. Sane Trilogy", "Dummy Game"]
    }

    recensionidict = {
        "testi": ["Questo gioco mi ha fatto molto divertire", "Gioco eccellente nella grafica", "Molto bello da esplorare", "Fantastico", "Mi piace molto questo gioco, mi ricorda la mia infanzia"],
        "voti": [10, 9.3, 8.4, 9.5, 10],
        "date_pubblicazione": [date(2021, 8, 23), date(2021, 12, 4), date(2022, 5, 1), date(2023, 6, 12), date(2023, 2, 7)],
        "utenti": ["Ritroder", "1TacticalBadger", "Abstract Lettuce", "IronMaidenEnjoyer", "Ritroder"],
        "prodotti": ["The Elder Scrolls V: Skyrim Special Edition", "The Elder Scrolls V: Skyrim Special Edition", "Minecraft", "Minecraft", "Crash Bandicoot N. Sane Trilogy"]
    }

    domandedict = {
        "testi": ["Qual'è il genere di questo videogioco?", "Ci sono i mostri?", "Quante ore dura la storia?", "Riesco a giocarlo con un Intel Core i5-13500?", "Quanti livelli ci sono?"],
        "risposte": ["RPG", "Si ci sono molti tipi di creature", "", "Si, se non installi troppe mod", ""],
        "utenti": ["Ritroder", "Ayaya", "IronMaidenEnjoyer", "Abstract Lettuce", "1TacticalBadger"],
        "utenti_risposte": ["1TacticalBadger", "Ritroder", "", "Ritroder", ""],
        "prodotti": ["The Elder Scrolls V: Skyrim Special Edition", "The Elder Scrolls V: Skyrim Special Edition", "Minecraft", "Minecraft", "Crash Bandicoot N. Sane Trilogy"]
    }

    # creazione tabelle
    gruppo_acquirenti = Group.objects.create(name="Acquirenti")
    gruppo_venditori = Group.objects.create(name="Venditori")

    for i in range(len(acquirentidict["nomi"])):
        u = CustomUser.objects.create_user(
            username=acquirentidict["nomi"][i],
            email=f"email{i}@email.com",
            password=make_password("password"))
        u.groups.add(gruppo_acquirenti)
        a = Acquirente()
        a.user = u
        for k in acquirentidict:
            if k == "nomi":
                a.nome = acquirentidict[k][i]
            if k == "foto":
                a.foto_profilo = acquirentidict[k][i]
            if k == "biografie":
                a.biografia = acquirentidict[k][i]
        a.save()

    for i in range(len(venditoridict["nomi"])):
        u = CustomUser.objects.create_user(
            username=venditoridict["nomi"][i],
            email=f"email{i}@email.com",
            password=make_password("password"))
        u.groups.add(gruppo_venditori)
        v = Venditore()
        v.user = u
        for k in venditoridict:
            if k == "nomi":
                v.nome = venditoridict[k][i]
            if k == "foto":
                v.foto_profilo = venditoridict[k][i]
        v.save()

    for i in range(len(prodottidict["titoli"])):
        p = Prodotto()
        for k in prodottidict:
            if k == "titoli":
                p.titolo = prodottidict[k][i]
            if k == "descrizioni":
                p.descrizione = prodottidict[k][i]
            if k == "prezzi":
                p.prezzo = prodottidict[k][i]
            if k == "requisiti":
                p.requisiti = prodottidict[k][i]
            if k == "date_rilascio":
                p.data_rilascio = prodottidict[k][i]
            if k == "generi":
                p.genere = prodottidict[k][i]
            if k == "venditori":
                p.venditore = Venditore.objects.get(nome=prodottidict[k][i])
            if k == "acquirenti":
                p.save()
                p.acquirenti.add(*(Acquirente.objects.filter(nome__in=prodottidict[k][i])))
        p.save()

    for i in range(len(recensionidict["testi"])):
        r = Recensione()
        for k in recensionidict:
            if k == "testi":
                r.testo = recensionidict[k][i]
            if k == "voti":
                r.voto = recensionidict[k][i]
            if k == "date_pubblicazione":
                r.data_pubblicazione = recensionidict[k][i]
            if k == "utenti":
                r.utente = Acquirente.objects.get(nome=recensionidict[k][i])
            if k == "prodotti":
                r.prodotto = Prodotto.objects.get(titolo=recensionidict[k][i])
        r.save()

    for i in range(len(domandedict["testi"])):
        d = Domanda()
        for k in domandedict:
            if k == "testi":
                d.testo = domandedict[k][i]
            if k == "risposte":
                d.risposta = domandedict[k][i]
            if k == "utenti":
                d.utente = Acquirente.objects.get(nome=domandedict[k][i])
            if k == "utenti_risposte" and d.risposta is not None:
                d.utente_risposta = Acquirente.objects.get(nome=domandedict[k][i])
            if k == "prodotti":
                d.prodotto = Prodotto.objects.get(titolo=domandedict[k][i])
        d.save()

    # dump del DB
    print("DUMP DB")
    print(CustomUser.objects.all())
    print(Acquirente.objects.all())
    print(Venditore.objects.all())
    print(Prodotto.objects.all())
    print(Recensione.objects.all())
    print(Domanda.objects.all())
