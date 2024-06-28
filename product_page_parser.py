'''Function for getting response text for product category pages'''

import asyncio
from urllib.parse import urlencode
import logging

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger("siteLogger")

async def get_and_parse(
        cat: str,
        url: str,
        params: dict,
        divclass: str,
        session: aiohttp.client.ClientSession,
        q: asyncio.Queue
) -> None:
    '''GET requests one page and parses it for getting all product listings
    using aiohttp and bs4
    define session in main'''


    async with session.get(url, params=params) as resp:
        full_url = f"{url}?{urlencode(params)}"
        logger.info("Accessing URL: %s", full_url)
        try:
            # when response is text
            html_text = await resp.text()
        except UnicodeDecodeError:
            # if response is in bytes
            html_text = await resp.read()

    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_=divclass)
    logger.debug("number of items in %s %s = %s", cat, params, len(items))
    await q.put((cat, items))
