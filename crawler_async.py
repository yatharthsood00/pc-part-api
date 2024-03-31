from bs4 import BeautifulSoup
from config import *

# universal crawler function 
async def fetch_page(session, sitename, url, params):
    
    # stripped-down async function
    # uses abstracted find_all class_ value,
    # hence why it needs the site in the def
    print(f"fetching url {url}, params {params}")
    async with session.get(url, params=params) as resp:
        html_text = await resp.text()

    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_=site_product_class[sitename])
    return items

# MDC crawler function 
# async def fetch_and_parse_page_mdc(url, session, params):
#     # needs a page-by-page loop per category
    
#     async with session.get(url, params=params) as response:
#         html_text = await response.text()

#     soup = BeautifulSoup(html_text, 'lxml')
#     items = soup.find_all('div', class_="product-wrapper")

#     return items