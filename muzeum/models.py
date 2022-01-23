from django.db import models
from django import forms
from django.contrib import messages
import warnings


class Instytucja(models.Model):
    nazwa = models.CharField(max_length=200, verbose_name="nazwa instytucji")
    miasto = models.CharField(max_length=200)

    def __str__(self):
        return self.nazwa

    # def clean(self):
    #     if self.nazwa == "a":
    #         raise forms.ValidationError("Hehe")

    class Meta:
        verbose_name_plural = "instytucje"


class Artysta(models.Model):
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    rok_urodzenia = models.PositiveSmallIntegerField(blank=False, null=False)
    rok_smierci = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.imie + " " + self.nazwisko

    class Meta:
        verbose_name_plural = "artysci"


class Eksponat(models.Model):
    class TypEksponatu(models.TextChoices):
        RZEZBA = 'rzezba'
        OBRAZ = 'obraz'
        INNY = 'inny'

    class Stan(models.TextChoices):
        WYPOZYCZONY = 'wypozyczony'
        W_EKSPOZYCJI = 'w ekspozycji'
        W_MAGAZYNIE = 'w magazynie'

    autor = models.ForeignKey(Artysta, blank=True, null=True, on_delete=models.SET_NULL)
    tytul = models.CharField(max_length=200, verbose_name="tytul eksponatu")
    typ = models.CharField(max_length=10, choices=TypEksponatu.choices)
    wypozyczalny = models.BooleanField(default=True, blank=False, null=False)
    stan = models.CharField(max_length=20, choices=Stan.choices)
    id_wypozyczenia = models.PositiveIntegerField(blank=True, null=True, default=None)
    id_ekspozycji = models.PositiveIntegerField(blank=True, null=True, default=None)
    szerokosc = models.PositiveIntegerField(default=0, blank=False, null=False)
    wysokosc = models.PositiveIntegerField(default=0, blank=False, null=False)
    waga = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.tytul

    class Meta:
        verbose_name_plural = "eksponaty"


class Wypozyczenie(models.Model):
    eksponat = models.ForeignKey(Eksponat, on_delete=models.DO_NOTHING)
    instytucja = models.ForeignKey(Instytucja, on_delete=models.DO_NOTHING)
    poczatek = models.DateField(blank=False, null=False)
    koniec = models.DateField(blank=False, null=False)

    def __str__(self):
        return self.instytucja.nazwa + ", " + self.eksponat.tytul + ", " + str(self.poczatek) + ' - ' + str(self.koniec)

    class Meta:
        verbose_name_plural = "wypozyczenia"


class Ekspozycja(models.Model):
    eksponat = models.ForeignKey(Eksponat, on_delete=models.DO_NOTHING)
    galeria = models.CharField(max_length=200)
    sala = models.CharField(max_length=200)
    poczatek = models.DateField(blank=False, null=False)
    koniec = models.DateField(blank=False, null=False)

    def __str__(self):
        return self.galeria + ", " + self.eksponat.tytul

    class Meta:
        verbose_name_plural = "ekspozycje"
