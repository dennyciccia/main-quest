# Generated by Django 5.0.6 on 2024-06-23 13:03

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodotti', '0001_initial'),
        ('utenti', '0007_alter_acquirente_foto_profilo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domanda',
            name='risposta',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='domanda',
            name='utente_risposta',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='risposte', to='utenti.acquirente'),
        ),
        migrations.AlterField(
            model_name='recensione',
            name='voto',
            field=models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
