import asyncio
import time

import aiohttp
from config import site_pages, site_params, pgb_categories
from crawler_async import fetch_page
from lister_async import lister_PGB

# removing links and other stuff, keep the for loop for PGB
# abstract the for loop and gather into another function
async def main():
    start_time = time.time()
    link = site_pages["PGB"]
    params = site_params["PGB"]
  
    async with aiohttp.ClientSession() as session:
        tasks = {}
        for cat, catlink in pgb_categories.items():
            task = fetch_page(session, "PGB", link + catlink, params)
            tasks[cat] = task

        responses = await asyncio.gather(*tasks.values())
        
        for cat, response in zip(tasks.keys(), responses):
            parsed_items = lister_PGB(response)
            print(f"Parsed items from {cat}: {len(parsed_items)}")
            # Process the parsed items further if needed

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")

# no touchy this
if __name__ == "__main__":
    # print("running")
    asyncio.run(main())
