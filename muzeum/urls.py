from datetime import datetime
from django.urls import path, register_converter
from . import views

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('', views.index, name='index'),
    path('artysci/', views.ArtistListView.as_view(), name='artysci'),
    path('eksponaty/', views.search_exhibits, name='szukaj_eksponaty'),
    path('eksponaty/<str:name>/<str:surname>/<str:state>/', views.show_exhibits, name='pokaz_eksponaty'),
    path('ekspozycje/', views.search_exhibitions, name='szukaj_ekspozycje'),
    path('ekspozycje/<str:exhibit>/<str:name>/<str:surname>/<yyyy:date>/', views.show_exhibitions, name='pokaz_ekspozycje'),
    path('wypozyczenia/', views.search_loans, name='szukaj_wypozyczenia'),
    path('wypozyczenia/<str:exhibit>/<str:name>/<str:surname>/<yyyy:date>/', views.show_loans, name='pokaz_wypozyczenia'),
]
