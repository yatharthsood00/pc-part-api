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
    SITEPAGES,
    CATEGORIES,
    SITE_PARAMS,
    DATABASEFILE,
    SitePack
)


async def get_and_parse(cat: str,
                        url_and_param: list[str, dict],
                        sitename: str,
                        session: aiohttp.client.ClientSession,
                        q: asyncio.Queue):
    '''GET requests one page and parses it for getting all product listings
    using aiohttp and bs4
    define session in main'''
    url = url_and_param[0]
    params = url_and_param[1]

    async with session.get(url, params=params) as resp:
        encoded_params = urlencode(params)
        full_url = f"{url}?{encoded_params}"
        print(f"Accessing URL: {full_url}")
        try:
            html_text = await resp.text()
        except UnicodeDecodeError:
            html_text = await resp.read()

    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_="product-wrapper")
    print(f"number of items in {cat} = {len(items)}")
    await q.put((cat, items))

async def create_listing(cursor, q: asyncio.Queue):
    """PGB lister from product listings"""
    while True:
        items_list = []

        category, markup_list = await q.get()

        for item in markup_list:
            # 1 - product name
            name = item.find('h3', class_="product-title").text.strip()

            # 2 - price
            price = item.find('span', class_='price').text
            try:
                # first from the two prices, remove the rupee, replace the comma (with nothing)
                price = price.split(" ")[0][1:].replace(",", "") 
                price = int(price)
            except ValueError:
                price = -1

            # 3 - instock indicator
            status = item.find('span', class_="out-of-stock")
            if status:
                stock = 0
            else:
                stock = 1

            # 4 - product link
            link = item.find('a', class_="woocommerce-LoopProduct-link")['href']

            items_list.append((name, link, price, stock, category))

        print(f"Category {category} - {len(items_list)} items listed") # db function can sort of directly go here

        for data in items_list:

            cursor.execute('''INSERT INTO pgb_products (
                                    name,
                                    link,
                                    price,
                                    instock,
                                    date,
                                    category
                                ) VALUES (?, ?, ?, ?, CURRENT_DATE, ?);''', data)
        
        print(f"Appended {category} to db")

        q.task_done()

async def create_pipeline(site):
    '''Main pipeline assembler
    Starts the ClientSession(), gets the URL list ready and passes to parser
    Then works on the parsed items further as required'''

    print(f"Starting pipeline for site {SITES[site]}")

    url_gen = SitePack(sitename = site)
    urls_and_params = url_gen.links_and_params

    session = aiohttp.ClientSession()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS pgb_products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT(200),
                        link VARCHAR,
                        price INTEGER,
                        instock INTEGER,
                        date DATE,
                        category text(30))
                    ;''')
    
    q = asyncio.Queue()

    product_markup_list = [asyncio.create_task(get_and_parse(cat, url_and_param, site, session, q))
                           for cat, url_and_param in urls_and_params.items()] # producers
    
    product_listings = [asyncio.create_task(create_listing(cursor, q))
                           for _ in range(len(urls_and_params))] # consumers
    
    await asyncio.gather(*product_markup_list)
    await q.join()

    # not needed as we are running every single producer and every single
    # consumer through the pipeline
    # for p in product_listings:
        # p.cancel()

    await session.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    asyncio.run(create_pipeline("PGB"))
