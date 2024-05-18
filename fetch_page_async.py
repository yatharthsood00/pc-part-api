"""Generic function for page fetching"""

from bs4 import BeautifulSoup
from config import site_product_class
from urllib.parse import urlencode

# universal crawler function
async def fetch_page(session, sitename, url, params):

    """stripped-down async function
    uses abstracted find_all class_ value,
    hence why it needs the site in the def
    Works for PGB, MDC (tested), ITD (probably)"""

    async with session.get(url, params=params) as resp:
        encoded_params = urlencode(params)
        full_url = f"{url}?{encoded_params}"
        print(f"Accessing URL: {full_url}")
        try:
            html_text = await resp.text()
        except UnicodeDecodeError:
            html_text = await resp.read()

    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_=site_product_class[sitename])
    print("number of items", len(items))
    return items
