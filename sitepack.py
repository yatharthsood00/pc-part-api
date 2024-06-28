'''SitePack class definition'''
import asyncio
import logging
import aiohttp
import re
from bs4 import BeautifulSoup

from config import (
    SITES,
    CATEGORIES,
    SITEPAGES,
    SITE_PARAMS
)

logger = logging.getLogger("sitepackLogger")

class SitePack:
    '''
    All-in-one class for all website-specific methods and parameters
    '''

    def __init__(
                self,
                sitename: str
            ) -> None:
        self.site = sitename
        self.full_sitename = SITES[self.site]
        self.categories = CATEGORIES[self.site]
        self.sitepage = SITEPAGES[self.site]

        '''
        divclass: Class of the div that has the product info (NLPI values)
        tablename: SQL table name
        '''

        if self.site == "PGB":
            self.divclass = 'product-wrapper'
            self.tablename = 'pgb_products'

        elif self.site == "ITD":
            self.divclass = 'product-item col-6 col-md-4 col-lg-3 p-1'
            self.tablename = 'itd_products'

        elif self.site == "MDC":
            self.divclass = 'right-block right-b'
            self.tablename = 'mdc_products'

        elif self.site == "PCS":
            self.divclass = 'jet-woo-products__item jet-woo-builder-product jet-woo-thumb-with-effect'
            self.tablename = 'pcs_products'

    async def parse_site(self) -> list[tuple]:
        '''
        Ladder to process paginated sites and non-paginated ones
        output format: dict
        {category -> str: [link-to-the-category -> str, params -> dict]}
        '''

        if self.site == "PGB":
            return self.parse_pgb()
        if self.site == "ITD":
            return self.parse_itd()
        if self.site == "MDC":
            return await self.parse_mdc()
        if self.site == "PCS":
            return await self.parse_pcs()

    def parse_pgb(self) -> list[tuple]:
        '''
        PGB style: link has category
        Simply append cat_append to base link
        '''

        urls = []
        site_params = SITE_PARAMS["PGB"] # static params for PGB
        for cat, cat_append in self.categories.items():
            link = f"{self.sitepage}{cat_append}"
            urls.append([cat, link, site_params])

        return urls

    def parse_itd(self) -> list[tuple]:
        '''
        ITD style: link has no category
        param changes for each category
        '''

        urls = []
        site_params = SITE_PARAMS["ITD"] # varying param "category", static sitepage
        for cat in self.categories.keys():
            params = site_params.copy()
            params["category"] = str(self.categories[cat])
            urls.append([cat, self.sitepage, params])

        return urls

    async def parse_mdc(self) -> list[tuple]:
        '''
        Main async process to create the MDC link list
        '''

        urls = []
        pagecounts = {}
        site_params = SITE_PARAMS["MDC"]

        pagecount_tasks = {cat: asyncio.create_task(self.get_pagecount_mdc(catlink))
                            for cat, catlink in self.categories.items()}
        await asyncio.gather(*pagecount_tasks.values())
        for cat, task in pagecount_tasks.items():
            result = await task
            pagecounts[cat] = result

        for cat, cat_append in self.categories.items():
            link = f"{self.sitepage}{cat_append}"
            pagecount = pagecounts[cat]
            logger.info("%s - %d pages", cat, pagecount)
            for i in range(1, pagecount+1):
                params = site_params.copy()
                params["page"] = i
                urls.append((cat, link, params))

        return urls
    
    async def parse_pcs(self) -> list[tuple]:
        '''
        Main async process to create the PCS link list
        '''

        urls = []
        pagecounts = {}
        site_params = SITE_PARAMS["PCS"]

        pagecount_tasks = {cat: asyncio.create_task(self.get_pagecount_pcs(catlink))
                            for cat, catlink in self.categories.items()}
        await asyncio.gather(*pagecount_tasks.values())
        for cat, task in pagecount_tasks.items():
            result = await task
            pagecounts[cat] = result

        for cat, cat_append in self.categories.items():
            link = f"{self.sitepage}{cat_append}"
            pagecount = pagecounts[cat]
            logger.info("%s - %d pages", cat, pagecount)
            for i in range(1, pagecount+1):
                params = site_params.copy()
                params["page"] = i
                urls.append((cat, link, params))

        return urls

    async def get_pagecount_mdc(self, link) -> int:
        '''
        Async process to get the pagecounts for each page in paginated sites
        '''

        logger.info("fetching for pagecount %s", self.sitepage+link)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.sitepage+link) as response:
                page_text = await response.text()
                soup = BeautifulSoup(page_text, 'lxml')
                page_text = soup.find("div", class_="col-sm-6 text-right").text.split(sep=" ")
        
        return int(page_text[6][1:])
    
    async def get_pagecount_pcs(self, link) -> int:
        '''
        Async process to find which page is the last one for each category
        a la PCS (var JetSmartFilterSettings, props, max_num_pages value)
        '''

        logger.info("fetching for pagecount %s", self.sitepage+link)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.sitepage+link) as response:
                pattern = re.compile(r'"max_num_pages":\s*(\d+)')
                page_text = await response.text()
                soup = BeautifulSoup(page_text, 'lxml')
                tag = soup.find('script', id='jet-smart-filters-js-extra').text
                pagecount = pattern.search(tag).group(1)

        return int(pagecount)

    def lister(self, html_block):
        '''
        Combined function for parsing all params to get
        defined product listing items
        '''

        name, link, price, stock = "", "", 0, 0

        if self.site == "PGB":
            # 1 - product name
            name = html_block.find("h3", class_="product-title").text.strip()

            # 2 - product link
            link = html_block.find('a', class_="woocommerce-LoopProduct-link")['href']

            # 3 - price
            price = html_block.find('span', class_='price').text
            try:
                price = price.split(" ")[-1][1:].replace(",", "")
                price = int(price)
            except ValueError:
                price = -1

            # 4 - instock indicator
            status = html_block.find('span', class_="out-of-stock")
            if not status:
                stock = 1


        elif self.site == "ITD":
            # 1 - product name
            name = html_block.find("a", class_="text-dark text-decoration-none")['title']

            # 2 - product link
            site = 'https://www.theitdepot.com/'
            link = site + html_block.find("a", class_="text-dark text-decoration-none")["href"]

            # 3 - price
            price = int(html_block.find("strong").text.strip())

            # 4 - instock indicator
            stock_tag = html_block.find("span", string="Out of Stock")
            if not stock_tag:
                stock = 1


        elif self.site == 'MDC':
            # 1 - product name
            name = html_block.find('h4').text

            # 2 - product link
            link = html_block.find('a')['href']

            # 3 - price
            price_str = html_block.find('span', class_="price-new").text.strip()
            price = price_str[1:].replace(",", "")
            price = int(price)

            # 4 - instock indicator
            stock = 1
        
        elif self.site == "PCS":
            # 1 - product name
            name = html_block.find('div', class_='jet-woo-product-title')['title']

            # 2 - product link
            link = html_block.find('div', class_='jet-woo-products__inner-box jet-woo-item-overlay-wrap')['data-url']

            # 3 - price
            try:
                price_str = html_block.find('div', class_='jet-woo-product-price').find('ins').text
                if price_str is None:
                    price = -1
                else:
                    price = int(float(price_str[1:].replace(",", "")))
                    
            except AttributeError:
                price = -1

            # 4 - instock indicator
            stock = 1

        return name, link, price, stock
    