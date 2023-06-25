# Unified code to get site title, product name and price from given PrimeABGB page (for means-testing)

import requests
from bs4 import BeautifulSoup

URLs = ["https://www.primeabgb.com/online-price-reviews-india/amd-ryzen-5-7600x-desktop-processor-100-100000593wof/",
        "https://www.primeabgb.com/online-price-reviews-india/gigabyte-b650-aorus-elite-ax-wifi-ddr5-am5-amd-motherboard/",
        "https://www.primeabgb.com/online-price-reviews-india/teamgroup-t-force-delta-rgb-32gb-16gbx2-ddr5-6000mhz-memory-white-ff4d532g6000hc38adc01/",
        "https://www.primeabgb.com/online-price-reviews-india/colorful-igame-geforce-rtx-4070-ultra-w-oc-v2-v-12gb-gddr6x-graphic-card/",
        "https://www.primeabgb.com/online-price-reviews-india/fractal-design-torrent-e-atx-black-solid-high-airflow-mid-tower-cabinet-fd-c-tor1a-05/",
        "https://www.primeabgb.com/online-price-reviews-india/fractal-design-pop-air-rgb-white-tg-clear-tint-tempered-glass-side-panel-mid-tower-cabinet-fd-c-por1a-01/"
        ]

for URL in URLs:
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, 'html5lib')

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
    targets["product_price"] = soup.select(f'{tags["price_tag"]}')[-1].text #.strip().split(" ")[-1]

    print(targets)
