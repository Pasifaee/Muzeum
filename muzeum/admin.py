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
            raise forms.ValidationError("Nieprawid??owe daty pocz??tku i ko??ca")
        if niedostepny(eksponat, poczatek, koniec, Wypozyczenie):
            raise forms.ValidationError(
                "Nie mo??na umie??ci?? dzie??a na ekspozycji, poniewa?? w podanym czasie jest ono wypo??yczone.")
        if niedostepny(eksponat, poczatek, koniec, Ekspozycja):
            raise forms.ValidationError(
                "W podanym czasie wybrane dzie??o znajduje si?? ju?? na ekspozycji.")


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
            raise forms.ValidationError("Nieprawid??owe daty pocz??tku i ko??ca.")
        if not eksponat.wypozyczalny:
            raise forms.ValidationError("Ten eksponat jest zbyt cenny, aby go wypo??yczy??.")

        if niedostepny(eksponat, poczatek, koniec, Wypozyczenie):
            raise forms.ValidationError(
                "Nie mo??na wypo??yczy?? eksponatu, poniewa?? w podanym czasie jest on ju?? wypo??yczony.")
        if niedostepny(eksponat, poczatek, koniec, Ekspozycja):
            raise forms.ValidationError(
                "Nie mo??na wypo??yczy?? eksponatu, poniewa?? w podanym czasie znajduje si?? on na ekspozycji.")
        if za_dlugie_wypozyczenie(eksponat, poczatek, koniec):
            raise forms.ValidationError(
                "Eksponat nie mo??e przebywa?? poza muzeum wi??cej ni?? 30 dni w ci??gu danego roku kalendarzowego.")


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
        raise forms.ValidationError("Nie mo??na umie??ci?? obiektu w magazynie, poniewa?? jest aktualnie wypo??yczony.")
    if len(Ekspozycja.objects.filter(poczatek__lte=datetime.date.today(), koniec__gte=datetime.date.today(),
                                     eksponat__tytul=tytul)) > 0:
        raise forms.ValidationError("Nie mo??na umie??ci?? obiektu w magazynie, poniewa?? aktualnie jest na ekspozycji.")


def ekspozycja_check(id_w, id_e, tytul):
    if id_w is not None:
        raise forms.ValidationError("Dzie??o na ekspozycji nie mo??e mie?? identyfikatora wypo??yczenia.")
    if id_e is None:
        raise forms.ValidationError("Dzie??o na ekspozycji musi posiada?? identyfikator ekspozycji.")
    try:
        iksde = Ekspozycja.objects.get(pk=id_w)
    except Ekspozycja.DoesNotExist:
        raise forms.ValidationError("Nieprawid??owy identyfikator ekspozycji: identyfikator nie istnieje.")
    if iksde.eksponat.tytul != tytul:
        raise forms.ValidationError(
            "Nieprawid??owy identyfikator ekspozycji: ekspozycja musi dotyczy?? wybranego eksponatu.")
    if datetime.date.today() < iksde.poczatek or datetime.date.today() > iksde.koniec:
        raise forms.ValidationError(
            "Dzie??o nie mo??e by?? aktualnie na ekspozycji: niezgodno???? dzisiejszej daty z okresem ekspozycji.")


def wypozyczony_check(id_w, id_e, tytul):
    if id_e is not None:
        raise forms.ValidationError("Wypo??yczony eksponat nie mo??e mie?? identyfikatora ekspozycji.")
    if id_w is None:
        raise forms.ValidationError("Wypo??yczony eksponat musi posiada?? identyfikator wypo??yczenia.")
    try:
        iksde = Wypozyczenie.objects.get(pk=id_w)
    except Wypozyczenie.DoesNotExist:
        raise forms.ValidationError("Nieprawid??owy identyfikator wypo??yczenia: identyfikator nie istnieje.")
    if iksde.eksponat.tytul != tytul:
        raise forms.ValidationError(
            "Nieprawid??owy identyfikator wypo??yczenia: wypo??yczenie musi dotyczy?? wybranego eksponatu.")
    if datetime.date.today() < iksde.poczatek or datetime.date.today() > iksde.koniec:
        raise forms.ValidationError(
            "Eksponat nie mo??e by?? aktualnie wypo??yczony: niezgodno???? dzisiejszej daty z okresem wypo??yczenia.")


class EksponatForm(ModelForm):
    def clean(self):
        stan = self.cleaned_data['stan']
        id_w = self.cleaned_data['id_wypozyczenia']
        id_e = self.cleaned_data['id_ekspozycji']
        tytul = self.cleaned_data['tytul']
        if stan == 'wypo??yczony':
            if not self.cleaned_data['wypozyczalny']:
                raise forms.ValidationError("Ten eksponat jest zbyt cenny by go wypo??yczy??.")
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
