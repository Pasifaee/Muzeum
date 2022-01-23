from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artysci/', views.ArtistListView.as_view(), name='artysci'),
    path('eksponaty/', views.search_exhibits, name='szukaj_eksponaty'),
    path('eksponaty/<str:name>/<str:surname>/', views.show_exhibits, name='pokaz_eksponaty')
]