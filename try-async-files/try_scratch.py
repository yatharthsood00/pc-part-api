import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup

async def fetch_and_parse_page(url, session, params):

    async with session.get(url, params=params) as response:
        html_text = await response.text()

    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_="product-wrapper")
    
    return items

def get_list_from_block_pgb(items):
    items_dict = {}
    for item in items:
        name = item.find("h3", class_="product-title").text.strip() 

        price = item.find('span', class_='price').text
        try:
            price = price.split(" ")[-1][1:].replace(",", "")
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
        
        items_dict[name] = {"price": price, "stock": stock, "link": link}

    return items_dict

async def main():
    link = "https://www.primeabgb.com/buy-online-price-india/category/"

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
    PGB = {'per_page': '9999'}

    link_list = []
    for cat in pgb_categories.values():
        link_list.append(link.replace("category", cat))

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_parse_page(url, session, params=PGB) for url in link_list]
        responses = await asyncio.gather(*tasks)

        for url, response in zip(link_list, responses):
            parsed_items = get_list_from_block_pgb(response)
            print(f"Parsed items from {url}: {len(parsed_items)}")
            # Process the parsed items further if needed

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main())
