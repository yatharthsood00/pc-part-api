# Test file to save page HTML (for finding data sources, etc. and to test properties, etc. for PrimeABGB

import requests
from bs4 import BeautifulSoup
import os

URLs = ["https://www.primeabgb.com/online-price-reviews-india/asus-tuf-a15-fa577rm-hf031ws-15-6-inch-amd-r7-6800h-rtx3060-6gb-8g8g-1t-ssd-15-6-fhd-300hz-gaming-laptop/",
        
]

for URL in URLs:
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, 'html5lib')
    with open(os.path.join(os.getcwd(), 'oos.html'), 'w') as file:
        file.write(soup.prettify())
    targets = {}

    properties = {
        "title_class": "product_title entry-title",
        "price_class": "price pewc-main-price"
    }

    tags = { # add as fstring
        "title_tag": "h1[class='product_title entry-title']",
        "price_tag": "p[class='price pewc-main-price']"
    }
    
    targets["product_title"] = soup.select(f'{tags["title_tag"]}')[-1].text.strip()
    # targets["product_price"] = soup.select(f'{tags["price_tag"]}') [-1].text.strip() #.split(" ")[-1]
    price_text = soup.find('li', class_='selling-price').text.strip()
    price_int = int(price_text[price_text.index("₹") + 1:].replace(",",""))
    print(price_int)
    # print(targets)
