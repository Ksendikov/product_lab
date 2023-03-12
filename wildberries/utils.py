import aiohttp

URL = 'https://card.wb.ru/cards/detail'


async def make_request(value):
    async with aiohttp.ClientSession() as sessions:
        async with sessions.get(f'{URL}?nm={value}') as response:
            return await response.json(content_type=None)
