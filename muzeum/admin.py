from django.contrib import admin

from .models import Eksponat, Artysta, Ekspozycja, Wypozyczenie, Instytucja

admin.site.site_header = 'Administracja muzeum'


class EkspozycjaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ['eksponat__tytul', 'eksponat__autor__imie', 'eksponat__autor__nazwisko']
    list_filter = ['poczatek', 'koniec', 'galeria', 'sala']

    def has_delete_permission(self, request, obj=None):
        return False


class WypozyczenieAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ['eksponat__tytul', 'instytucja__nazwa', 'eksponat__autor__imie', 'eksponat__autor__nazwisko']
    list_filter = ['poczatek', 'koniec', 'eksponat__tytul', 'instytucja__nazwa']

    def has_delete_permission(self, request, obj=None):
        return False


class EksponatAdmin(admin.ModelAdmin):
    search_fields = ['tytul', 'autor__imie', 'autor__nazwisko']
    list_filter = ['typ', 'stan']

    def has_delete_permission(self, request, obj=None):
        return False


class ArtystaAdmin(admin.ModelAdmin):
    search_fields = ['imie', 'nazwisko']

    def has_delete_permission(self, request, obj=None):
        return False


class InstytucjaAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Ekspozycja, EkspozycjaAdmin)
admin.site.register(Wypozyczenie, WypozyczenieAdmin)
admin.site.register(Eksponat, EksponatAdmin)
admin.site.register(Artysta, ArtystaAdmin)
admin.site.register(Instytucja, InstytucjaAdmin)
