# Generated by Django 5.0.6 on 2024-06-13 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utenti', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='editore',
            options={'verbose_name_plural': 'Editori'},
        ),
        migrations.AlterModelOptions(
            name='sviluppatore',
            options={'verbose_name_plural': 'Sviluppatori'},
        ),
        migrations.AlterModelOptions(
            name='utente',
            options={'verbose_name_plural': 'Utenti'},
        ),
    ]
