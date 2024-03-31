import requests
from bs4 import BeautifulSoup
import time
from functools import wraps
from time import time
import threading

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func%r took: %2.4f sec' % (f.__name__, te-ts))
        return result
    return wrap

def timing_average(n):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            total_time = 0.0
            for _ in range(n):
                ts = time()
                result = f(*args, **kwargs)
                te = time()
                total_time += (te - ts)
            avg_time = total_time / n
            print('func %r averaged %2.4f sec over %d runs' % (f.__name__, avg_time, n))
            return result
        return wrap
    return decorator

def get_response_pgb(link, params, result_holder, event):
    response = requests.get(link, params=params)
    result_holder['response'] = response
    event.set()

def pgb_page_soup(response):
    soup = BeautifulSoup(response.text, 'html5lib')
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
        
        status = item.find('span', class_="out-of-stock")
        if status:
            stock = 0
        else:
            stock = 1
        
        link = item.find('a', class_="woocommerce-LoopProduct-link")['href']
    return items_dict

def process_response_threaded(result_holder, event):
    event.wait()
    response = result_holder['response']
    items = pgb_page_soup(response)
    items_dict = get_list_from_block_pgb(items)
    result_holder['items'] = items_dict

@timing
def put_all_together(lk, cat):
    print(f"\n{cat}")
    result_holder = {}
    event = threading.Event()
    thread1 = threading.Thread(target=get_response_pgb, args=(lk, PGB, result_holder, event))
    thread2 = threading.Thread(target=process_response_threaded, args=(result_holder, event))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    # Do something with the results if needed

PGB = {'per_page': '9999'}
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

for cat in pgb_categories.values():
    lk = link.replace("category", cat)

    put_all_together(lk, cat)

