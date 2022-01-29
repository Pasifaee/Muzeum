import datetime
from django import forms

class SearchArtistsForm(forms.Form):
    artist_name = forms.CharField(label='Imię artysty', required=False)
    artist_surname = forms.CharField(label='Nazwisko artysty', required=False)

TYPE_CHOICES = (('dowolny', 'dowolny'), ('obraz', 'obraz'), ('rzezba', 'rzezba'), ('inny', 'inny'))
STATE_CHOICES = (('dowolny', 'dowolny'), ('wypozyczony', 'wypozyczony'), ('w ekspozycji', 'w ekspozycji'), ('w magazynie', 'w magazynie'))
class SearchExhibitsForm(forms.Form):
    exhibit_name = forms.CharField(label='Nazwa eksponatu', required=False)
    author_name = forms.CharField(label='Imię autora', required=False)
    author_surname = forms.CharField(label='Nazwisko autora', required=False)
    type = forms.ChoiceField(label='Rodzaj', choices=TYPE_CHOICES, required=False)
    state = forms.ChoiceField(label='Stan', choices=STATE_CHOICES, required=False)


class SearchExhibitionsForm(forms.Form):
    exhibit = forms.CharField(label='Nazwa eksponatu', required=False)
    author_name = forms.CharField(label='Imię autora', required=False)
    author_surname = forms.CharField(label='Nazwisko autora', required=False)
    date = forms.DateField(label='Data', required=False, help_text='Wybierz dzień, w którym chciałbyś wybrać się do galerii. Wpisz datę w formacie yyyy-mm-dd.')


class SearchLoansForm(forms.Form):
    exhibit = forms.CharField(label='Nazwa eksponatu', required=False)
    author_name = forms.CharField(label='Imię autora', required=False)
    author_surname = forms.CharField(label='Nazwisko autora', required=False)
    date = forms.DateField(label='Data', required=False, help_text='Wyświetlimy wypożyczenia trwające w wybranym przez ciebie dniu. Wpisz datę w formacie yyyy-mm-dd.')
