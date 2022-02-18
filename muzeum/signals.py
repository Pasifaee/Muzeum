import datetime

from django.forms import forms
from django.db.models.signals import post_save
from muzeum.models import Wypozyczenie, Ekspozycja, Eksponat
from django.dispatch import receiver


@receiver(post_save, sender=Wypozyczenie)
def zmien_stan(sender, instance, **kwargs):
    if instance.poczatek <= datetime.date.today() <= instance.koniec:
        ziomal = Eksponat.objects.get(pk=instance.eksponat.id)
        ziomal.id_ekspozycji = None
        ziomal.id_wypozyczenia = instance.id
        ziomal.stan = 'wypożyczony'
        ziomal.save()


@receiver(post_save, sender=Ekspozycja)
def zmien_stan(sender, instance, **kwargs):
    if instance.poczatek <= datetime.date.today() <= instance.koniec:
        ziomal = Eksponat.objects.get(pk=instance.eksponat.id)
        ziomal.id_wypozyczenia = None
        ziomal.id_ekspozycji = instance.id
        ziomal.stan = 'w ekspozycji'
        ziomal.save()
