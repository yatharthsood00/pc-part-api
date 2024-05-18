"""Asynchronous version of main script to run the program from
*Async script for PGB parts only"""

import asyncio

import aiohttp
from config import site_pages, site_params, pgb_categories

from fetch_page_async import fetch_page
from lister_async import lister_pgb


async def crawler_pgb():

    """ main running function, should
    ideally one-by-one run all scripts
    defines a session, imports all params
    and goes for it """

    link = site_pages["PGB"]
    params = site_params["PGB"]
    async with aiohttp.ClientSession() as session:
        tasks = {}
        for cat, catlink in pgb_categories.items():
            task = fetch_page(session, "PGB", link + catlink, params)
            tasks[cat] = task

        responses = await asyncio.gather(*tasks.values())
        for cat, response in zip(tasks.keys(), responses):
            parsed_items = lister_pgb(response)
            print(f"Parsed count from {cat}: {len(parsed_items)}")
            # Process the parsed items further if needed

    return parsed_items

if __name__ == "__main__":
    # print("running")
    list_of_items = asyncio.run(crawler_pgb())
    # print(list_of_items)
    # l = lister_pgb(list_of_items)
    # print(list_of_items["Thermaltake Toughpower GF3 A3 1050 Watt 80 Plus
    # Gold ATX 3.0 SMPS PS-TPD-1050FNFAGD-H"])
