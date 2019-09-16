from django import forms

from cardpicker.models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('dbf_id', 'name', 'player_class')
