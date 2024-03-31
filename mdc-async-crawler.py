from bs4 import BeautifulSoup
from config import *
import requests
import sys
import time
import asyncio
import aiohttp
from crawler_async import fetch_page
from lister_async import lister_MDC

async def mdc_fetch_pagecount(session, category_link):
    print(f"getting pagecount for {category_link}")
    link = site_pages["MDC"] + category_link
    async with session.get(link) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        page_text = soup.find("div", class_="col-sm-6 text-right").text
        pagecount = int(page_text.split()[6][1:])
        return pagecount

async def mdc_fetch_category(session, category, page):
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
            # like the original synchronous function
        pagecount_tasks = [mdc_fetch_pagecount(session, category_link) for category_link in mdc_categories.values()]
        pagecounts = await asyncio.gather(*pagecount_tasks)
        tasks = []
        for category, pagecount in zip(mdc_categories, pagecounts):
            category_tasks = [mdc_fetch_category(session, category, page) for page in range(1, pagecount + 1)]
            tasks.extend(category_tasks)

        all_items = await asyncio.gather(*tasks)

        for category_items in all_items:
            for item in category_items:
                blocks.append(item)
                # HTML Request and processing to BS4
                # print("requesting", link, params)
                # response = requests.get(link, params=params)
                # soup = BeautifulSoup(response.text, 'lxml')
                # items = soup.find_all('div', class_="right-block right-b")
                # if len(items) == 0: # can we if less than 25 then that's it
                #     break
                # print(f"found {len(items)} items")
                # # append to blocks
                # for item in items:
                #     blocks.append((item, category))
                # if len(items) < 25:
                #     break

    return blocks

if __name__ == "__main__":
    st = time.time()
    list_ofallitems = asyncio.run(crawler_MDC())
    print(type(list_ofallitems))
    et = time.time()
    print(f"fetch time {et-st}")
    st = time.time()
    l = lister_MDC(list_ofallitems)
    et = time.time()
    print(f"parse time {et-st}")
    print(l)