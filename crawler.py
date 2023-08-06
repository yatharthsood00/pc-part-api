import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
from lister import ProductListing

# variables, keep them here
from config import *

class SiteCrawler:
    def __init__(self, sitename):
        self.site = sitename

        if self.site == "PGB":
            self.blocks = self.page_PGB()
        elif self.site == "ITD":
            self.blocks = self.page_ITD()
        elif self.site == "MDC":
            self.blocks = self.page_MDC()

    def page_PGB(self):

        blocks = [] 

        for category in pgb_categories:

            # prepare GET request parameters
            link = site_pages["PGB"] + pgb_categories[category]
            params = site_params["PGB"]

            # make GET request
            response = requests.get(link, params=params)
            
            # Find all html blocks
            soup = BeautifulSoup(response.text, 'html5lib')
            items = soup.find_all('div', class_="product-wrapper")

            # add to blocks with category and stuff
            for item in items:
                blocks.append((self.site, item, category))

        return blocks
    
    def page_ITD(self):

        blocks = []

        for category in itd_categories:

            # load link and params for ITD
            params = site_params["ITD"]
            params["category"] = str(itd_categories[category])
            link = site_pages["ITD"]

            # HTTPS request
            response = requests.post(link, params=params , verify=False)
            soup = BeautifulSoup(response.text, 'html5lib')

            # All HTML blocks
            items = soup.find_all("div", class_="product-item col-6 col-md-4 col-lg-3 p-1")

            # add to blocks with category and stuff
            for item in items:
                blocks.append((self.site, item, category))

        return blocks

    def page_MDC(self):
        
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
                    blocks.append((self.site, item, category))

        return blocks

