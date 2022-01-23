from django.shortcuts import render
from django.views import generic
from .models import Artysta, Eksponat, Ekspozycja, Wypozyczenie


def index(request):
    """Strona główna"""
    return render(request, 'index.html')

class ArtistListView(generic.ListView):
    model = Artysta
    context_object_name = 'artist_list'
    template_name = 'muzeum/artysci.html'