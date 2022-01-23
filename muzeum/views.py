from django.shortcuts import render
from .models import Artysta, Eksponat, Ekspozycja, Wypozyczenie


def index(request):
    """Home page"""
    return render(request, 'index.html')
