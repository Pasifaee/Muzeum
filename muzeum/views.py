from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Artysta, Eksponat, Ekspozycja, Wypozyczenie
from .forms import SearchExhibitsForm


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
            url = reverse('pokaz_eksponaty', kwargs={'name': name, 'surname': surname})
            # redirect to a new URL:
            # return HttpResponseRedirect('/muzeum/eksponaty/%s/%s/' % name % surname)
            return HttpResponseRedirect(url)

    # If this is a GET (or any other method) create the default form.
    else:
        form = SearchExhibitsForm()

    context = {
        'form': form,
    }

    return render(request, 'muzeum/eksponaty.html', context)


def show_exhibits(request, name, surname):
    exhibits_list = Eksponat.objects.all()

    ## Losowy przykład manipulowania wynikiem w zależności od danych wejściowych (w tym wypadku od name)
    if name == "-":
        exhibits_list = exhibits_list.filter(tytul__exact="whatever")
    ## Trzeba będzie go zastąpić sensownym filtrowaniem wyników.

    context = {
        'exhibits_list': exhibits_list,
    }

    return render(request, 'eksponaty_pokaz.html', context)
