'''
Script triggered from here
'''

import asyncio
import sqlite3
import logging
import time

import aiohttp
from sitepack import SitePack
from product_page_parser import get_and_parse
from listing_creator import create_listing
from config import (
    SITES,
    DATABASEFILE,
    CREATE_QUERY_TEMPLATE
)

logger = logging.getLogger("mainLogger")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# logger.propagate = False


async def create_pipeline(site_to_refresh):
    '''
    Main pipeline assembler
    Starts the ClientSession(), gets the URL list ready and passes to parser
    Then works on the parsed items further as required
    '''

    sp = SitePack(sitename = site_to_refresh)

    logger.info("Starting pipeline for site %s", sp.full_sitename)

    # can remove from this function, need to just open these once
    sess = aiohttp.ClientSession()
    conn = sqlite3.connect(DATABASEFILE)
    cursor = conn.cursor()
    q = asyncio.Queue()

    cursor.execute(CREATE_QUERY_TEMPLATE.format(tablename=sp.tablename))

    list_of_links = await sp.parse_site()

    product_markup_list = [asyncio.create_task(get_and_parse(cat, link, param,
                                                             sp.divclass, sess, q))
                           for cat, link, param in list_of_links] # producers

    _ = [asyncio.create_task(create_listing(sp, cursor, q))
                           for _ in range(len(list_of_links))] # consumers

    await asyncio.gather(*product_markup_list)
    await q.join()

    conn.commit() # commit SQL changes

    # clean up - can also be moved out
    await sess.close() # close ClientSession()
    conn.close() # close SQLite Connection

    logger.info("Pipeline for site %s now closed", SITES[site_to_refresh])

if __name__ == "__main__":

    # runtime flags can be used here
    refresh_list = ["PGB", "ITD", "MDC"]
    for site in refresh_list:
        start_time = time.perf_counter()
        asyncio.run(create_pipeline(site))
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.debug("Elapsed time for %s: %.2f seconds", site, elapsed_time)
