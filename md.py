# Test file to save page HTML (for finding data sources, etc. and to test properties, etc. for MDComputers 

import requests
from bs4 import BeautifulSoup
import os

URLs = ["https://mdcomputers.in/fractal-design-era-gold-m-itx-mini-tower.html",
        "https://mdcomputers.in/amd-ryzen-5-7600-100-100001015box.html"
]

for URL in URLs:
    resp = requests.get(URL)
    print(resp.status_code)
    soup = BeautifulSoup(resp.text, 'html5lib')

    title_property = "meta[property='og:title']"
    price_property = "meta[property='product:price:amount']"
    oos_tag = "div[class='stock']"

    title_tag = soup.select_one(title_property)
    title = title_tag.get('content')
    print(title)
    
    price_tag = soup.select_one(price_property)
    price = price_tag.get('content')
    print(price)

    stock_div = soup.select_one(oos_tag).text
    stock_status = stock_div.split(sep=":")[1].strip()
    print(stock_status)
