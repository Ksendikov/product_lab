from django.core.exceptions import ValidationError
from rest_framework import serializers

from wildberries.models import Card
from wildberries.utils import get_card_info, get_cards_info


class CardSerializer(serializers.Serializer):
    article = serializers.IntegerField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if 'article' in validate_data and 'file' in validate_data:
            raise ValidationError({'two_field_error': 'Only one field should be filled in'})
        elif 'article' not in validate_data and 'file' not in validate_data:
            raise ValidationError({'none_field_error': 'The field for article or file must be filled in.'})
        return attrs

    def save(self, **kwargs):
        article = self.validated_data.pop('article', None)
        file = self.validated_data.pop('file', None)
        if file:
            cards = get_cards_info(file)
            for i in cards:
                if 'article' in i:
                    if not Card.objects.filter(article=i.article).exists():
                        Card.objects.create(**i.dict())
                    else:
                        Card.objects.filter(article=i.article).update(brand=i.brand, title=i.title)
            return cards
        elif article:
            card = get_card_info(article)
            if 'article' in card:
                if not Card.objects.filter(article=card.article).exists():
                    Card.objects.create(**card.dict())
                else:
                    Card.objects.filter(article=card.article).update(brand=card.brand, title=card.title)
                return card
