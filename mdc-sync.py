from bs4 import BeautifulSoup
from config import *
import requests
import sys

import time

def page_MDC():
        
    blocks = []

    for category in mdc_categories:
        
        # prep for first request (number of pages)
        link = site_pages["MDC"] + mdc_categories[category]
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html5lib')
        page = soup.find("div", class_="col-sm-6 text-right").text.split(sep=" ")
        pages = int(page[6][1:]) # number of pages received from here

        for page in range(1, pages + 1):
            # prep link here:
            link = site_pages["MDC"] + mdc_categories[category]
            params = site_params["MDC"]
            params["page"] = page

            # HTML Request and processing to BS4
            response = requests.get(link, params=params)
            soup = BeautifulSoup(response.text, 'html5lib')
            items = soup.find_all('div', class_="right-block right-b")

            # append to blocks
            for item in items:
                blocks.append((item, category))

    return blocks

st = time.time()
page_MDC()
et = time.time()
print(et-st)