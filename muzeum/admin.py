import datetime

from django.contrib import admin
from django.forms import forms, ModelForm
from django.contrib.auth.models import Group, User

from .models import Eksponat, Artysta, Ekspozycja, Wypozyczenie, Instytucja

admin.site.site_header = 'Administracja muzeum'


def niedostepny(eksponat, poczatek, koniec, typ):
    kolizje_1 = len(typ.objects.filter(eksponat=eksponat, poczatek=poczatek))
    kolizje_2 = len(typ.objects.filter(eksponat=eksponat, poczatek__lt=poczatek).exclude(koniec__lt=poczatek))
    kolizje_3 = len(typ.objects.filter(eksponat=eksponat, poczatek__gt=poczatek).exclude(poczatek__gt=koniec))
    return kolizje_1 or kolizje_2 or kolizje_3


def dni_w_roku(eksponat, rok):
    grupa1 = Wypozyczenie.objects.filter(eksponat=eksponat, poczatek__year=rok, koniec__year=rok)
    grupa2 = Wypozyczenie.objects.filter(eksponat=eksponat, poczatek__year=rok - 1, koniec__year=rok)
    grupa3 = Wypozyczenie.objects.filter(eksponat=eksponat, poczatek__year=rok, koniec__year=rok + 1)
    dni = 0
    for wypozyczenie in grupa1:
        dni += (wypozyczenie.koniec - wypozyczenie.poczatek).days + 1

    for wypozyczenie in grupa2:
        dni += (wypozyczenie.koniec - datetime.date(rok, 1, 1)).days + 1

    for wypozyczenie in grupa3:
        dni += (datetime.date(rok + 1, 1, 1) - wypozyczenie.poczatek).days

    return dni


def za_dlugie_wypozyczenie(eksponat, poczatek, koniec):
    if poczatek.year == koniec.year:
        dni = (koniec - poczatek).days + 1
        if dni > 30:
            return True
        else:
            return dni_w_roku(eksponat, poczatek.year) + dni > 30
    else:
        dni1 = (datetime.date(koniec.year, 1, 1) - poczatek).days
        dni2 = (koniec - datetime.date(koniec.year, 1, 1)).days + 1
        if dni1 > 30 or dni2 > 30:
            return True
        else:
            return dni_w_roku(eksponat, poczatek.year) + dni1 > 30 or \
                   dni_w_roku(eksponat, koniec.year) + dni2 > 30


class EkspozycjaForm(ModelForm):
    def clean(self):
        poczatek = self.cleaned_data['poczatek']
        koniec = self.cleaned_data['koniec']
        eksponat = self.cleaned_data['eksponat']
        if koniec < poczatek:
            raise forms.ValidationError("Nieprawidłowe daty początku i końca")
        if niedostepny(eksponat, poczatek, koniec, Wypozyczenie):
            raise forms.ValidationError(
                "Nie można umieścić dzieła na ekspozycji, ponieważ w podanym czasie jest ono wypożyczone.")
        if niedostepny(eksponat, poczatek, koniec, Ekspozycja):
            raise forms.ValidationError(
                "W podanym czasie wybrane dzieło znajduje się już na ekspozycji.")


@admin.register(Ekspozycja)
class EkspozycjaAdmin(admin.ModelAdmin):
    form = EkspozycjaForm
    readonly_fields = ('id',)
    search_fields = ['id', 'eksponat__tytul', 'eksponat__autor__imie', 'eksponat__autor__nazwisko']
    list_filter = ['poczatek', 'koniec', 'galeria', 'sala']

    def has_delete_permission(self, request, obj=None):
        return False


class WypozyczenieForm(ModelForm):
    def clean(self):
        poczatek = self.cleaned_data['poczatek']
        koniec = self.cleaned_data['koniec']
        eksponat = self.cleaned_data['eksponat']
        if koniec < poczatek:
            raise forms.ValidationError("Nieprawidłowe daty początku i końca.")
        if not eksponat.wypozyczalny:
            raise forms.ValidationError("Ten eksponat jest zbyt cenny, aby go wypożyczyć.")

        if niedostepny(eksponat, poczatek, koniec, Wypozyczenie):
            raise forms.ValidationError(
                "Nie można wypożyczyć eksponatu, ponieważ w podanym czasie jest on już wypożyczony.")
        if niedostepny(eksponat, poczatek, koniec, Ekspozycja):
            raise forms.ValidationError(
                "Nie można wypożyczyć eksponatu, ponieważ w podanym czasie znajduje się on na ekspozycji.")
        if za_dlugie_wypozyczenie(eksponat, poczatek, koniec):
            raise forms.ValidationError(
                "Eksponat nie może przebywać poza muzeum więcej niż 30 dni w ciągu danego roku kalendarzowego.")


@admin.register(Wypozyczenie)
class WypozyczenieAdmin(admin.ModelAdmin):
    form = WypozyczenieForm
    readonly_fields = ('id',)
    search_fields = ['id', 'eksponat__tytul', 'instytucja__nazwa', 'eksponat__autor__imie',
                     'eksponat__autor__nazwisko']
    list_filter = ['poczatek', 'koniec', 'eksponat__tytul', 'instytucja__nazwa']

    def has_delete_permission(self, request, obj=None):
        return False


def magazyn_check(tytul):
    if len(Wypozyczenie.objects.filter(poczatek__lte=datetime.date.today(), koniec__gte=datetime.date.today(),
                                       eksponat__tytul=tytul)) > 0:
        raise forms.ValidationError("Nie można umieścić obiektu w magazynie, ponieważ jest aktualnie wypożyczony.")
    if len(Ekspozycja.objects.filter(poczatek__lte=datetime.date.today(), koniec__gte=datetime.date.today(),
                                     eksponat__tytul=tytul)) > 0:
        raise forms.ValidationError("Nie można umieścić obiektu w magazynie, ponieważ aktualnie jest na ekspozycji.")


def ekspozycja_check(id_w, id_e, tytul):
    if id_w is not None:
        raise forms.ValidationError("Dzieło na ekspozycji nie może mieć identyfikatora wypożyczenia.")
    if id_e is None:
        raise forms.ValidationError("Dzieło na ekspozycji musi posiadać identyfikator ekspozycji.")
    try:
        iksde = Ekspozycja.objects.get(pk=id_w)
    except Ekspozycja.DoesNotExist:
        raise forms.ValidationError("Nieprawidłowy identyfikator ekspozycji: identyfikator nie istnieje.")
    if iksde.eksponat.tytul != tytul:
        raise forms.ValidationError(
            "Nieprawidłowy identyfikator ekspozycji: ekspozycja musi dotyczyć wybranego eksponatu.")
    if datetime.date.today() < iksde.poczatek or datetime.date.today() > iksde.koniec:
        raise forms.ValidationError(
            "Dzieło nie może być aktualnie na ekspozycji: niezgodność dzisiejszej daty z okresem ekspozycji.")


def wypozyczony_check(id_w, id_e, tytul):
    if id_e is not None:
        raise forms.ValidationError("Wypożyczony eksponat nie może mieć identyfikatora ekspozycji.")
    if id_w is None:
        raise forms.ValidationError("Wypożyczony eksponat musi posiadać identyfikator wypożyczenia.")
    try:
        iksde = Wypozyczenie.objects.get(pk=id_w)
    except Wypozyczenie.DoesNotExist:
        raise forms.ValidationError("Nieprawidłowy identyfikator wypożyczenia: identyfikator nie istnieje.")
    if iksde.eksponat.tytul != tytul:
        raise forms.ValidationError(
            "Nieprawidłowy identyfikator wypożyczenia: wypożyczenie musi dotyczyć wybranego eksponatu.")
    if datetime.date.today() < iksde.poczatek or datetime.date.today() > iksde.koniec:
        raise forms.ValidationError(
            "Eksponat nie może być aktualnie wypożyczony: niezgodność dzisiejszej daty z okresem wypożyczenia.")


class EksponatForm(ModelForm):
    def clean(self):
        stan = self.cleaned_data['stan']
        id_w = self.cleaned_data['id_wypozyczenia']
        id_e = self.cleaned_data['id_ekspozycji']
        tytul = self.cleaned_data['tytul']
        if stan == 'wypożyczony':
            if not self.cleaned_data['wypozyczalny']:
                raise forms.ValidationError("Ten eksponat jest zbyt cenny by go wypożyczyć.")
            wypozyczony_check(id_w, id_e, tytul)
        elif stan == 'w ekspozycji':
            ekspozycja_check(id_w, id_e, tytul)
        else:
            magazyn_check(tytul)


@admin.register(Eksponat)
class EksponatAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    form = EksponatForm
    search_fields = ['tytul', 'autor__imie', 'autor__nazwisko']
    list_filter = ['typ', 'stan']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Artysta)
class ArtystaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ['imie', 'nazwisko']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Instytucja)
class InstytucjaAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Group)
admin.site.unregister(User)
