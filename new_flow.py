'''New implementation of asyncio queue for one website
Could be expanded to all apps together
Functions will be re-imported
Using the producer-consumer design pattern'''

import asyncio
from urllib.parse import urlencode
import sqlite3

import aiohttp
from bs4 import BeautifulSoup
from config import (
    SITES,
    DATABASEFILE,
)
from sitepack import SitePack


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

async def create_listing(sp: SitePack, cursor, q: asyncio.Queue):
    """PGB lister from product listings"""
    while True:
        items_list = []

        category, markup_list = await q.get()

        for item in markup_list:
            name, link, price, stock = sp.lister(item)
            items_list.append((name, link, price, stock, category))

        print(f"Category {category} - {len(items_list)} items listed") # lister finished, db next

        for data in items_list:

            cursor.execute(f'''INSERT INTO {sp.tablename} (
                                    name,
                                    link,
                                    price,
                                    instock,
                                    date,
                                    category
                                ) VALUES (?, ?, ?, ?, CURRENT_DATE, ?);''', data)

        print(f"Appended {category} to db")

        q.task_done()

async def create_pipeline(site_to_refresh):
    '''Main pipeline assembler
    Starts the ClientSession(), gets the URL list ready and passes to parser
    Then works on the parsed items further as required'''

    print(f"Starting pipeline for site {SITES[site_to_refresh]}")

    sp = SitePack(sitename = site_to_refresh)
    sess = aiohttp.ClientSession()
    conn = sqlite3.connect(DATABASEFILE)
    cursor = conn.cursor()

    q = asyncio.Queue()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {sp.tablename} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT(200),
                        link VARCHAR,
                        price INTEGER,
                        instock INTEGER,
                        date DATE,
                        category text(30))
                    ;''')

    product_markup_list = [asyncio.create_task(get_and_parse(cat, link, param,
                                                             sp.divclass, sess, q))
                           for cat, link, param in sp.links_and_params] # producers

    _ = [asyncio.create_task(create_listing(sp, cursor, q))
                           for _ in range(len(sp.links_and_params))] # consumers

    await asyncio.gather(*product_markup_list)
    await q.join()

    conn.commit() # commit SQL changes

    # clean up
    await sess.close() # close ClientSession()
    conn.close() # close SQLite Connection

if __name__ == "__main__":

    refresh_list = ["PGB", "ITD", "MDC"]
    for site in refresh_list:
        asyncio.run(create_pipeline(site))
