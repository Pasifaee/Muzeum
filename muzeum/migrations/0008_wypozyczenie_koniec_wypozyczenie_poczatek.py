# Generated by Django 4.0.1 on 2022-01-21 23:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('muzeum', '0007_ekspozycja_koniec_ekspozycja_poczatek'),
    ]

    operations = [
        migrations.AddField(
            model_name='wypozyczenie',
            name='koniec',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wypozyczenie',
            name='poczatek',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
