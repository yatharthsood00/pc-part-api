'''Function for getting response text for product category pages'''

import asyncio
from urllib.parse import urlencode

import aiohttp
from bs4 import BeautifulSoup

async def get_and_parse(
                        cat: str,
                        url: str,
                        params: dict,
                        divclass: str,
                        session: aiohttp.client.ClientSession,
                        q: asyncio.Queue):
    '''GET requests one page and parses it for getting all product listings
    using aiohttp and bs4
    define session in main'''


    async with session.get(url, params=params) as resp:
        encoded_params = urlencode(params)
        full_url = f"{url}?{encoded_params}"
        print(f"Accessing URL: {full_url}")
        try:
            html_text = await resp.text()
        except UnicodeDecodeError:
            html_text = await resp.read()

    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_=divclass)
    print(f"number of items in {cat} {params} = {len(items)}")
    await q.put((cat, items))