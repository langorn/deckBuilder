from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('draw/', views.build_deck, name='build_deck'),
    path('decks/', views.decks, name='decks')
]
