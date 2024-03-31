import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup
from config import *
from crawler_async import fetch_page
from lister_async import lister_MDC


async def mdc_fetch_pagecount(session, category_link):

    # For each category, get the page counts
    # from the page number test.
    # Executed asynchronously, all pagecounts are fetched
    # concurrently.

    # print(f"getting pagecount for {category_link}")
    link = site_pages["MDC"] + category_link
    async with session.get(link) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        page_text = soup.find("div", class_="col-sm-6 text-right").text
        # gets you "Showing 1 to 12 of 12 (1 Pages)"
        pagecount = int(page_text.split()[6][1:])
        # gets you the value after bracket open, cast to int
        return pagecount

async def mdc_fetch_category(session, category, page):

    # Helper function to fetch all pages
    # from a particular category

    link = site_pages["MDC"] + mdc_categories[category]
    params = site_params["MDC"]
    params["page"] = page

    return await fetch_page(session, "MDC", link, params)

async def crawler_MDC():
    async with aiohttp.ClientSession() as session:
        blocks = []

        # as pagination is hardcoded in MDC
        # need to first get the exact page number of each category
        # and use that in the pagewise loop

        pagecount_tasks = [mdc_fetch_pagecount(session, cat) for cat in mdc_categories.values()]
        pagecounts = await asyncio.gather(*pagecount_tasks)

        # collecting product listings
        # ALL pages fetched concurrently
        tasks = []
        for category, pagecount in zip(mdc_categories, pagecounts):
            category_tasks = [mdc_fetch_category(session, category, page) for page in range(1, pagecount + 1)]
            tasks.extend(category_tasks)
        all_items = await asyncio.gather(*tasks)

        for category_items in all_items:
            for item in category_items:
                blocks.append(item)

    return blocks

if __name__ == "__main__":

    list_ofallitems = asyncio.run(crawler_MDC())
    l = lister_MDC(list_ofallitems)

