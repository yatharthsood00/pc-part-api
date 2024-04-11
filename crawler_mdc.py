"""Async Script for crawling all MDComputers products """

import asyncio

import aiohttp
from bs4 import BeautifulSoup
from config import site_pages, mdc_categories, site_params

from fetch_page_async import fetch_page
from lister_async import lister_mdc


async def mdc_fetch_pagecount(session, category_link):

    """For each category, get the page counts
    from the page number test.
    Executed asynchronously, all pagecounts are fetched
    concurrently."""

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

    """Helper function to fetch all pages
    from a particular category"""

    link = site_pages["MDC"] + mdc_categories[category]
    params = site_params["MDC"]
    params["page"] = page

    return await fetch_page(session, "MDC", link, params)

async def crawler_mdc():

    """Web crawler function after getting ready 
    the page numbers"""

    async with aiohttp.ClientSession() as session:
        listings = []

        # as pagination is hardcoded in MDC
        # need to first get the exact page number of each category
        # and use that in the pagewise loop

        pagecount_tasks = [mdc_fetch_pagecount(session, cat) for cat in mdc_categories.values()]
        pagecounts = await asyncio.gather(*pagecount_tasks)
        print("Page counts:", pagecounts)
        # collecting product listings
        # ALL pages fetched concurrently
        tasks = {}
        for category, pagecount in zip(mdc_categories, pagecounts):
            category_tasks = [mdc_fetch_category(session, category, page)
                              for page in range(1, pagecount + 1)]
            tasks[category] = category_tasks
        print(tasks.values())
        all_items = await asyncio.gather(*[task for category_tasks in tasks.values()
                                          for task in category_tasks])

        for category_items in all_items:
            print(f"items in category: {len(category_items)}")
            for item in category_items:
                listings.append(item)

    return listings

if __name__ == "__main__":

    list_ofallitems = asyncio.run(crawler_mdc())
    print(len(list_ofallitems))
    l = lister_mdc(list_ofallitems)
    # print(l)
