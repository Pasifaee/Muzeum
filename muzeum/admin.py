from django.contrib import admin

from .models import Eksponat, Artysta, Ekspozycja, Wypozyczenie, Instytucja

admin.site.site_header = 'Administracja muzeum'


class EkspozycjaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class WypozyczenieAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Ekspozycja, EkspozycjaAdmin)
admin.site.register(Wypozyczenie, WypozyczenieAdmin)
admin.site.register(Eksponat)
admin.site.register(Artysta)
admin.site.register(Instytucja)
