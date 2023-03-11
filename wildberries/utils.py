import aiohttp


async def make_request(value):
    async with aiohttp.ClientSession() as sessions:
        async with sessions.get(f'https://card.wb.ru/cards/detail?nm={value}') as response:
            return await response.json(content_type=None)


