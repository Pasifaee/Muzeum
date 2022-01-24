from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Artysta, Eksponat, Ekspozycja, Wypozyczenie
from .forms import SearchExhibitsForm, SearchExhibitionsForm, SearchLoansForm


def index(request):
    """Strona główna"""
    return render(request, 'index.html')


class ArtistListView(generic.ListView):
    model = Artysta
    context_object_name = 'artist_list'
    template_name = 'muzeum/artysci.html'


def search_exhibits(request):
    """Strona dla przeszukujących dane o eksponatach."""
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchExhibitsForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            name = form.cleaned_data['author_name']
            surname = form.cleaned_data['author_surname']
            if not name: name = 'blank'
            if not surname: surname = 'blank'
            state = form.cleaned_data['state']
            url = reverse('pokaz_eksponaty', kwargs={'name': name, 'surname': surname, 'state': state})
            # redirect to a new URL:
            return HttpResponseRedirect(url)

    # If this is a GET (or any other method) create the default form.
    else:
        form = SearchExhibitsForm()

    context = {
        'form': form,
    }

    return render(request, 'muzeum/eksponaty.html', context)


def show_exhibits(request, name, surname, state):
    exhibits_list = Eksponat.objects.all()

    authors = Artysta.objects.all()
    if name != 'blank':
        authors = authors.filter(imie__icontains=name)
    if surname != 'blank':
        authors = authors.filter(nazwisko__icontains=surname)

    if name != 'blank' or surname != 'blank':
        exhibits_list = exhibits_list.filter(autor_id__in=authors)

    if state != 'dowolny':
        exhibits_list = exhibits_list.filter(stan__exact=state)

    exhibits_list_full = []
    for exhibit in exhibits_list:
        author = authors.get(id=exhibit.autor_id)
        exhibits_list_full.append([exhibit, author])

    context = {
        'exhibits_list': exhibits_list_full,
    }

    return render(request, 'eksponaty_pokaz.html', context)


def search_exhibitions(request):
    """Strona dla przeszukujących dane o eksponatach."""
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchExhibitionsForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            exhibit = form.cleaned_data['exhibit']
            name = form.cleaned_data['author_name']
            surname = form.cleaned_data['author_surname']
            if not exhibit: exhibit = 'blank'
            if not name: name = 'blank'
            if not surname: surname = 'blank'
            date = form.cleaned_data['date']
            if not date:
                url = reverse('pokaz_ekspozycje',
                              kwargs={'exhibit': exhibit, 'name': name, 'surname': surname})
            else:
                url = reverse('pokaz_ekspozycje_data', kwargs={'exhibit': exhibit, 'name': name, 'surname': surname, 'date': date})
            # redirect to a new URL:
            return HttpResponseRedirect(url)

    # If this is a GET (or any other method) create the default form.
    else:
        form = SearchExhibitionsForm()

    context = {
        'form': form,
    }

    return render(request, 'muzeum/ekspozycje.html', context)


def show_exhibitions(request, exhibit, name, surname, date=None):
    exhibitions_list = Ekspozycja.objects.all()

    # Trzeba tu dodać przefiltrowanie exhibitions_list na podstawie argumentów

    context = {
        'exhibitions_list': exhibitions_list,
    }

    return render(request, 'ekspozycje_pokaz.html', context)


def search_loans(request):
    """Strona dla przeszukujących dane o eksponatach."""
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchLoansForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            exhibit = form.cleaned_data['exhibit']
            name = form.cleaned_data['author_name']
            surname = form.cleaned_data['author_surname']
            if not exhibit: exhibit = 'blank'
            if not name: name = 'blank'
            if not surname: surname = 'blank'
            date = form.cleaned_data['date']
            if not date:
                url = reverse('pokaz_wypozyczenia', kwargs={'exhibit': exhibit, 'name': name, 'surname': surname})
            else:
                url = reverse('pokaz_wypozyczenia_data', kwargs={'exhibit': exhibit, 'name': name, 'surname': surname, 'date': date})
            # redirect to a new URL:
            return HttpResponseRedirect(url)

    # If this is a GET (or any other method) create the default form.
    else:
        form = SearchLoansForm()

    context = {
        'form': form,
    }

    return render(request, 'muzeum/wypozyczenia.html', context)


def show_loans(request, exhibit, name, surname, date=None):
    loans_list = Wypozyczenie.objects.all()

    # Trzeba tu dodać przefiltrowanie loans_list na podstawie argumentów

    context = {
        'loans_list': loans_list,
    }

    return render(request, 'wypozyczenia_pokaz.html', context)
