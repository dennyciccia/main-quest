# Generated by Django 5.0.6 on 2024-06-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utenti', '0007_alter_acquirente_foto_profilo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquirente',
            name='foto_profilo',
            field=models.ImageField(default='imgs/default_profile_image.png', upload_to='profile_pics/'),
        ),
    ]
