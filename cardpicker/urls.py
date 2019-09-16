from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('draw/', views.draw, name='draw'),
    path('decks/', views.decks, name='decks')
]
