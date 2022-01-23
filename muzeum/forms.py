import datetime
from django import forms

STATE_CHOICES = (('wypozyczony', 'wypozyczony'), ('w ekspozycji', 'w ekspozycji'), ('w magazynie', 'w magazynie'))
class SearchExhibitsForm(forms.Form):
    author_name = forms.CharField(label='Imię autora', required=False)
    author_surname = forms.CharField(label='Nazwisko autora', required=False)
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
