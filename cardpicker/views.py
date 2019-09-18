# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from backend import CardDealer
import requests

dealer = CardDealer()

def index(request):
    return render(request,'index.html', {})
# Create your views here.

def api_call():
    response = dealer.api_call()
    return response

def build_deck(request):
    hand_cards = dealer.build_deck()
    save_deck(hand_cards)
    return JsonResponse(hand_cards, safe=False)

def save_deck(hand_cards):
    dealer.save_deck(hand_cards)
    return HttpResponseRedirect('/')

def decks(request):
    data = dealer.show_deck()
    return JsonResponse(data, safe=False)
