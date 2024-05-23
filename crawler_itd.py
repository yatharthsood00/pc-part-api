"""Async Script for crawling ITDepot Products"""

import asyncio

import aiohttp
from bs4 import BeautifulSoup
from config import SITEPAGES, SITE_PARAMS, itd_categories

from fetch_page_async import fetch_page

async def crawler_itd():

    """ main running function, should
    ideally one-by-one run all scripts
    defines a session, imports all params
    and goes for it """

    link = SITEPAGES["ITD"]
    params_template = SITE_PARAMS["ITD"]


    async with aiohttp.ClientSession() as session:
        tasks = {}
        for cat, catlink in itd_categories.items():
            params = params_template.copy()
            params["category"] = str(catlink)
            task = fetch_page(session, "ITD", link, params)
            tasks[cat] = task

        responses = await asyncio.gather(*tasks.values())
        for cat, response in zip(tasks.keys(), responses):
            print(len(response))
            # parsed_items = lister_pgb(response)
            # print(f"Parsed count from {cat}: {len(parsed_items)}")
            # Process the parsed items further if needed

    return ""

if __name__ == "__main__":
    # print("running")
    list_of_items = asyncio.run(crawler_itd())
