# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import JsonResponse
import random
from django.shortcuts import render
from cardpicker.forms import CardForm
from django.http import HttpResponseRedirect
from django.core import serializers
from cardpicker.models import Card
import json

import requests

def index(request):
    return HttpResponse("Hello world, you're at the healthstone index.")
# Create your views here.

def api_call():
    print('api_call')
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/sets/Rastakhan%27s%20Rumble"
    headers = {
        'X-Mashape-Key': "ZTMJtzbYvXmshPTFEZI4ztIy3I68p1nPwgHjsnIGukKZeJxGcs",
    }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return response.json()

def check_duplicate(hand_card_set, current_card):
    count = 0
    result = False
    for card in hand_card_set:
        if card['cardId'] == current_card['cardId']:
            print(card['cardId'], current_card['cardId'])
            count += 1

    # if same card more than 2, dont give it 1 more this type of card.
    if count >= 1:
        print('this card duplicate', card['cardId'])
        result = True
    return result


def draw(request):

    player_class = 'Hunter'
    cards = api_call()
    hand_card_no = 0
    hand_card_set = []
    max_count = 0

    while hand_card_no < 30:
        # random pick one card in this api
        item = random.choice(cards)

        # if not belong to our player class , skip it. pick another
        if 'playerClass' in item and item['playerClass'] != 'Hunter':
            pass
        elif 'playerClass' not in item:
            pass
        else:
            is_duplicate = check_duplicate(hand_card_set, item)

            if not is_duplicate:
                hand_card_no += 1
                hand_card_set.append( item )

    saveDeck(hand_card_set)
    return JsonResponse('ok', safe=False)

def saveDeck(hand_card_set):
    resetDesk()
    for card_set in hand_card_set:
        dataset = {
            'dbf_id': card_set['dbfId'],
            'name': card_set['name'],
            'player_class': card_set['playerClass']
        }

        card_form = CardForm(dataset)
        if card_form.is_valid():
            form = card_form.save(commit=False)
            form.save()
        else:
            print('failed')

    return HttpResponseRedirect('/')

def resetDesk():
    Card.objects.all().delete()
    return HttpResponse()

def decks(self):
    result = Card.objects.all()
    data = serializers.serialize('json', result)
    return HttpResponse(data, content_type="application/json")
