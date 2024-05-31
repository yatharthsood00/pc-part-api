'''Script triggered from here
TODO: add flags to determine sites to run script for'''

import asyncio
import sqlite3
import logging

import aiohttp
from config import (
    SITES,
    DATABASEFILE,
)
from sitepack import SitePack
from product_page_parser import get_and_parse
from listing_creator import create_listing

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("mainLogger")
logger.propagate = False  # Disable propagation for the main logger
logger.addHandler(logging.getLogger("parserLogger"))


async def create_pipeline(site_to_refresh):
    '''Main pipeline assembler
    Starts the ClientSession(), gets the URL list ready and passes to parser
    Then works on the parsed items further as required'''

    logger.info("Starting pipeline for site %s", SITES[site_to_refresh])

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

    logger.info("Pipeline for site %s now closed", SITES[site_to_refresh])

if __name__ == "__main__":

    refresh_list = ["PGB", "ITD", "MDC"]
    for site in refresh_list:
        asyncio.run(create_pipeline(site))