from django.db import models


class Instytucja(models.Model):
    nazwa = models.CharField(max_length=200)
    miasto = models.CharField(max_length=200)

    def __str__(self):
        return self.nazwa


class Artysta(models.Model):
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    rok_urodzenia = models.PositiveSmallIntegerField
    rok_smierci = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.imie + " " + self.nazwisko


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
    tytul = models.CharField(max_length=200)
    typ = models.CharField(max_length=10, choices=TypEksponatu.choices)
    wypozyczalny = models.BooleanField
    stan = models.CharField(max_length=20, choices=Stan.choices)
    id_wypozyczenia = models.PositiveIntegerField(blank=True, null=True)
    id_ekspozycji = models.PositiveIntegerField(blank=True, null=True)
    szerokosc = models.PositiveIntegerField
    wysokosc = models.PositiveIntegerField
    waga = models.PositiveIntegerField

    def __str__(self):
        return self.tytul


class Wypozyczenie(models.Model):
    id_eksponatu = models.ForeignKey(Eksponat, on_delete=models.DO_NOTHING)
    id_instytucji = models.ForeignKey(Instytucja, on_delete=models.DO_NOTHING)
    poczatek = models.DateField
    koniec = models.DateField

    def __str__(self):
        return self.id_instytucji.nazwa + ", " + self.id_eksponatu.tytul


class Ekspozycja(models.Model):
    id_eksponatu = models.ForeignKey(Eksponat, on_delete=models.DO_NOTHING)
    galeria = models.CharField(max_length=200)
    sala = models.CharField(max_length=200)
    poczatek = models.DateField
    koniec = models.DateField

    def __str__(self):
        return self.galeria + ", " + self.id_eksponatu.tytul
