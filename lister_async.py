from bs4 import BeautifulSoup

def lister_PGB(items):
    items_dict = {}
    for item in items:
        name = item.find("h3", class_="product-title").text.strip()

        price = item.find('span', class_='price').text
        try:
            price = price.split(" ")[-1][1:].replace(",", "")
            price = int(price)
        except ValueError:
            price = -1

        # 3 - instock indicator
        status = item.find('span', class_="out-of-stock")
        if status:
            stock = 0
        else:
            stock = 1

        # 4 - product link
        link = item.find('a', class_="woocommerce-LoopProduct-link")['href']

        items_dict[name] = {"price": price, "stock": stock, "link": link}

    return items_dict

def lister_MDC(items):
    items_dict = {}
    for item in items:
        # 1 - product name
        name = item.find('h4').text

        # 2 - price
        price_str = item.find('span', class_="price-new").text.strip()
        price = price_str[1:].replace(",", "")
        price = int(price) 

        # 3 - instock indicator
        stock = 1 

        # 4 - product link
        link = item.find('a')['href']

        items_dict[name] = {"price": price, "stock": stock, "link": link}

    return items_dict