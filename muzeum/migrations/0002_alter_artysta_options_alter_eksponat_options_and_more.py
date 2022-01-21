# Generated by Django 4.0.1 on 2022-01-21 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muzeum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artysta',
            options={'verbose_name_plural': 'artysci'},
        ),
        migrations.AlterModelOptions(
            name='eksponat',
            options={'verbose_name_plural': 'eksponaty'},
        ),
        migrations.AlterModelOptions(
            name='ekspozycja',
            options={'verbose_name_plural': 'ekspozycje'},
        ),
        migrations.AlterModelOptions(
            name='instytucja',
            options={'verbose_name_plural': 'instytucje'},
        ),
        migrations.AlterModelOptions(
            name='wypozyczenie',
            options={'verbose_name_plural': 'wypozyczenia'},
        ),
        migrations.AddField(
            model_name='artysta',
            name='rok_urodzenia',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]