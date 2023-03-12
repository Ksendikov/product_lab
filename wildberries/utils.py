import asyncio
import json

import aiohttp
from openpyxl import load_workbook

from wildberries.pydantic import CardPydantic

URL = 'https://card.wb.ru/cards/detail'


async def make_request(value):
    async with aiohttp.ClientSession() as sessions:
        async with sessions.get(f'{URL}?nm={value}') as response:
            return await response.json(content_type=None)


def get_card_info(value):
    page = asyncio.run(make_request(value))
    return get_objects(page, value)


def get_cards_info(file):
    values = []
    wb = load_workbook(file)
    for sheet in wb.sheetnames:
        for row in wb[sheet].iter_rows(values_only=True):
            values.append(row[0])
    cards_info = [get_card_info(i) for i in values]
    return cards_info


def get_objects(page, value):
    card = None
    try:
        products = json.dumps(page['data']['products'][0])
        card = CardPydantic.parse_raw(products)
    except IndexError:
        print(f'article {value} not found')
    if card:
        return card
    else:
        return {'error': value}
