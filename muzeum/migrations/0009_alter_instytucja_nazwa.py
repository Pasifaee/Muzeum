# Generated by Django 4.0.1 on 2022-01-22 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muzeum', '0008_wypozyczenie_koniec_wypozyczenie_poczatek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instytucja',
            name='nazwa',
            field=models.CharField(max_length=200, verbose_name='nazwa instytucji'),
        ),
    ]
