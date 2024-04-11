"""Generic function for page fetching"""

from bs4 import BeautifulSoup
from config import site_product_class

# universal crawler function
async def fetch_page(session, sitename, url, params):

    """stripped-down async function
    uses abstracted find_all class_ value,
    hence why it needs the site in the def
    Works for PGB, MDC (tested), ITD (probably)"""

    async with session.get(url, params=params) as resp:
        html_text = await resp.text()

    soup = BeautifulSoup(html_text, 'lxml')
    items = soup.find_all('div', class_=site_product_class[sitename])
    return items
