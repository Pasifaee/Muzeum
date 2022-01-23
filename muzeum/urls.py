from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artysci/', views.ArtistListView.as_view(), name='artysci'),
]