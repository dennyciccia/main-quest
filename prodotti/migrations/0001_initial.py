# Generated by Django 5.0.6 on 2024-06-14 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utenti', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prodotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=100)),
                ('descrizione', models.TextField()),
                ('prezzo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('requisiti', models.CharField(max_length=500)),
                ('data_rilascio', models.DateField()),
                ('acquirenti', models.ManyToManyField(related_name='prodotti', to='utenti.utente')),
                ('editore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prodotti', to='utenti.editore')),
                ('sviluppatore', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prodotti', to='utenti.sviluppatore')),
            ],
            options={
                'verbose_name_plural': 'Prodotti',
            },
        ),
        migrations.CreateModel(
            name='Immagine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='')),
                ('testo_alternativo', models.CharField(max_length=100)),
                ('prodotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='immagini', to='prodotti.prodotto')),
            ],
            options={
                'verbose_name_plural': 'Immagini',
            },
        ),
        migrations.CreateModel(
            name='Domanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testo', models.CharField(max_length=500)),
                ('risposta', models.CharField(blank=True, max_length=500)),
                ('utente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='domande', to='utenti.utente')),
                ('utente_risposta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='risposte', to='utenti.utente')),
                ('prodotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domande', to='prodotti.prodotto')),
            ],
            options={
                'verbose_name_plural': 'Domande',
            },
        ),
        migrations.CreateModel(
            name='Recensione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testo', models.TextField(blank=True)),
                ('voto', models.DecimalField(decimal_places=1, max_digits=10)),
                ('data_pubblicazione', models.DateField()),
                ('prodotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recensioni', to='prodotti.prodotto')),
                ('utente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recensioni', to='utenti.utente')),
            ],
            options={
                'verbose_name_plural': 'Recensioni',
            },
        ),
    ]