'''Function to save each product listing value
from product listing markup segments'''

import asyncio
from sitepack import SitePack

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