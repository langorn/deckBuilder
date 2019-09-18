import requests
import random
from django.http import HttpResponse
from cardpicker.forms import CardForm
from cardpicker.models import Card
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)

class CardDealer:
    def __init__(self):
        pass


    def api_call(self):
        print('api_call')
        url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/sets/Rastakhan%27s%20Rumble"
        headers = {
            'X-Mashape-Key': "ZTMJtzbYvXmshPTFEZI4ztIy3I68p1nPwgHjsnIGukKZeJxGcs",
        }
        response = requests.request("GET", url, headers=headers)
        return response.json()


    def show_deck(self):
        result = Card.objects.all()
        data = self.reconstruct(result)
        print(data)
        return data

    def reset_desk(self):
        Card.objects.all().delete()
        return HttpResponse()


    def build_deck(self):
        player_class = 'Hunter'
        cards = self.api_call()
        hand_card_no = 0
        hand_card_set = []
        max_count = 0

        # keep pick card before 30 cards on hand.
        while hand_card_no < 30:
            # random pick one card in this api
            item = random.choice(cards)

            # if not belong to our player class , skip it. pick another
            if 'playerClass' not in item:
                pass
            # our class & neutral card only
            elif item['playerClass'] == 'Hunter' or item['playerClass'] == 'Neutral':
                is_duplicate = self.check_duplicate(hand_card_set, item)

                if not is_duplicate:
                    hand_card_no += 1
                    hand_card_set.append( item )
        return hand_card_set


    def save_deck(self, hand_cards):
        self.reset_desk()
        for card_set in hand_cards:
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
        return


    def check_duplicate(self, hand_card_set, current_card):
        count = 0
        result = False
        for card in hand_card_set:
            if card['cardId'] == current_card['cardId']:
                print(card['cardId'], current_card['cardId'])
                count += 1

        # if same card more than 2, dont give it more this type of card.
        if count >= 2:
            print('this card duplicate', card['cardId'])
            result = True
        return result


    def reconstruct(self, items):
    	items_collections = []
    	for item in items:
    		card = {
    			'dbf_id':item.dbf_id,
    			'name': item.name,
    			'player_class':item.player_class
    		}
    		items_collections.append(card)
    	return items_collections
