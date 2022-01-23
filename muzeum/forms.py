from django import forms


class SearchExhibitsForm(forms.Form):
    author_name = forms.CharField(label="Imię autora")
    author_surname = forms.CharField(label="Nazwisko autora")
