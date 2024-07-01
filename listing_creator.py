'''Function to save each product listing value
from product listing markup segments'''

import asyncio
import logging
from sitepack import SitePack

logger = logging.getLogger("parserLogger")

async def create_listing(sp: SitePack, cursor, q: asyncio.Queue):
    """
    Universal lister for all product listings
    """

    while True:
        items_list = []

        category, markup_list = await q.get()

        for item in markup_list:
            name, link, price, stock = sp.lister(item)
            items_list.append((name, link, price, stock, category))

        logger.info("Parsed page for Category %s - %d items found",
                    category, len(items_list))

        for data in items_list:

            cursor.execute(f'''INSERT INTO {sp.tablename} (
                                    name,
                                    link,
                                    price,
                                    instock,
                                    date,
                                    category
                                ) VALUES (?, ?, ?, ?, CURRENT_DATE, ?);''', data)

        logger.info("Appended Category %s to db", category)

        q.task_done()
