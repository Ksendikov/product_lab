import json
from rest_framework.views import APIView
from rest_framework.response import Response
from openpyxl import load_workbook
import requests
from wildberries.pydantic import CardPydantic
import aiohttp

session = aiohttp.ClientSession()


class CardView(APIView):
    @staticmethod
    async def get_card_info_async(value):
        params = {'nm': value}
        async with session.get('https://card.wb.ru/cards/detail', params=params) as resp:
            await print(resp.status)

    @staticmethod
    def get_card_info(value):

        page = requests.get(f'https://card.wb.ru/cards/detail?nm={value}')
        return CardView.get_objects(page, value)

    @staticmethod
    def get_cards_info(file):
        values = []
        wb = load_workbook(file)
        for sheet in wb.sheetnames:
            for row in wb[sheet].iter_rows(values_only=True):
                values.append(row[0])
        cards_info = [CardView.get_card_info(i) for i in values]
        asunc_card = CardView.get_card_info_async(values[0])
        return cards_info

    @staticmethod
    def get_objects(page, value):
        card = None
        try:
            card = CardPydantic.parse_raw(json.dumps(page.json()['data']['products'][0]))
        except IndexError as e:
            print(f'id {value} отсутствует на сайте wildberries.ru')
        if card:
            return card.dict()
        else:
            return {'error': f'id {value} отсутствует на сайте wildberries.ru'}

    def post(self, request, *args, **kwargs):
        data = None
        if 'file'  in request.data and 'value' in request.data:
            return Response({'error': 'Одновременно отправлять поля file и value запрещено!'})
        elif 'file' in request.data:
            file = request.data['file']
            data = CardView.get_cards_info(file)
        elif 'value' in request.data:
            value = request.data['value']
            data = CardView.get_card_info(value)
        return Response(data)


