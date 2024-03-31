from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time

from functools import wraps

def timing(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {round((end_time - start_time), 4)} seconds")
        return result
    return wrapper

def timing_average(n):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            total_time = 0.0
            for _ in range(n):
                ts = time()
                result = f(*args, **kwargs)
                te = time()
                total_time += (te - ts)
            avg_time = total_time / n
            print('func %r averaged %2.4f sec over %d runs' % (f.__name__, avg_time, n))
            return result
        return wrap
    return decorator

async def get_response_pgb(session, link, params):
    async with session.get(link, params=params) as response:
        return await response.text()

async def pgb_page_soup(html):
    soup = BeautifulSoup(html, 'html5lib')
    items = soup.find_all('div', class_="product-wrapper")
    return items

async def get_list_from_block_pgb(item):
    name = item.find("h3", class_="product-title").text.strip() 

    price = item.find('span', class_='price').text
    try:
        price = price.split(" ")[-1][1:].replace(",", "")
        price = int(price)
    except ValueError:
        price = -1
    
    status = item.find('span', class_="out-of-stock")
    stock = 0 if status else 1

    link = item.find('a', class_="woocommerce-LoopProduct-link")['href']
    
    return {'name': name, 'price': price, 'stock': stock, 'link': link}

@timing
async def fetch_items_pgb(session, link, params):
    async with session.get(link, params=params) as response:
        html = await response.text()
        items_task = pgb_page_soup(html)  # Start pgb_page_soup asynchronously
        items = await items_task  # Wait for pgb_page_soup to complete
        tasks = [get_list_from_block_pgb(item) for item in items]
        results = await asyncio.gather(*tasks)
        return results

async def main():
    link = "https://www.primeabgb.com/buy-online-price-india/category/"
    PGB = {'per_page': '9999'}
    pgb_categories = {
        "Processor": "cpu-processor",
        "Cooler": "cpu-cooler",
        "Motherboard": "motherboards",
        "Memory": "ram-memory",
        "SSD": "ssd",
        "HDD": "internal-hard-drive",
        "GPU": "graphic-cards-gpu",
        "Case": "pc-cases-cabinet",
        "PSU": "power-supplies-smps",
        "Monitor": "led-monitors",
    }

    async with aiohttp.ClientSession() as session:
        for cat in pgb_categories.values():
            print(f"\n{cat}")
            lk = link.replace("category", cat)
            items = await fetch_items_pgb(session, lk, PGB)
            # print(items)  # You can process the items here

asyncio.run(main())

