import asyncio

from django.core.exceptions import ValidationError
from rest_framework import serializers

from wildberries.utils import (get_card_info, get_cards_info,
                               update_or_create_card)


class CardSerializer(serializers.Serializer):
    article = serializers.IntegerField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, attrs):
        validate_data = super().validate(attrs)
        error_two_field = {
            'error_two_field':
                'Only one field should be filled in'
        }
        error_none_field = {
            'error_none_field':
                'The field for article or file must be filled in'
        }

        if 'article' in validate_data and 'file' in validate_data:
            raise ValidationError(error_two_field)
        elif 'article' not in validate_data and 'file' not in validate_data:
            raise ValidationError(error_none_field)
        return attrs

    def save(self, **kwargs):
        article = self.validated_data.pop('article', None)
        file = self.validated_data.pop('file', None)
        if file:
            cards = asyncio.run(get_cards_info(file))
            for card in cards:
                return update_or_create_card(card)
        card = get_card_info(article)
        return update_or_create_card(card)
