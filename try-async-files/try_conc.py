import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time

async def fetch(session, url, params):
    async with session.get(url, params=params) as response:
        print(f"fetching link {url}")
        return await response.text()

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="product-wrapper")
    parsed_items = []
    for item in items:
        name = item.find("h3", class_="product-title").text.strip()
        price = item.find('span', class_='price').text.split()[-1][1:].replace(",", "")
        price = int(price) if price.isdigit() else -1
        stock = 0 if item.find('span', class_="out-of-stock") else 1
        link = item.find('a', class_="woocommerce-LoopProduct-link")['href']
        parsed_items.append({'name': name, 'price': price}) #, 'stock': stock, 'link': link})
    return parsed_items

async def main():
    PGB = {'per_page': '9999'}
    base_url = "https://www.primeabgb.com/buy-online-price-india/category/"

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
        tasks = []
        for cat, path in pgb_categories.items():
            url = base_url + path
            print(f"\nFetching {cat}...")
            start_time = time.time()
            # tasks.append(fetch(session, url))  # No need for this line
            html = await fetch(session, url, params=PGB)
            print(f"Parsing {cat}...")
            processed_items = parse(html)
            end_time = time.time()
            print(f"{cat} parsed in {end_time - start_time:.2f} seconds")
            # print(*processed_items, sep="\n")

asyncio.run(main())
