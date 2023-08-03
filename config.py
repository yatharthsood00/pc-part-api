# Meta stuff, for reference
sitenames = {'primeabgb': 'PGB', 'mdcomputers': 'MDC', 'theitdepot': 'ITD'}
website_tables = {
                  "theitdepot": "itd_products",
                  "mdcomputers": "md_products",
                  "primeabgb": "prime_products"
                }

# categories! to get through all products for itdepot. Can add categories here to get more products,
# for now only the most obvious candidates stay here
itd_category_dict = {
    "Cabinets": 5,
    "Cooling": 10,
    "Graphics Cards": 45,
    "HDDs": 12,
    "Memory": 6,
    "Monitors": 7,
    "Motherboards": 13,
    "PSU": 14,
    "Procesors": 30,
    "SSDs": 93,
    "Laptops": 27,
}

# Main Variables
site_pages = {
    "PGB": "https://www.primeabgb.com/buy-online-price-india/",
    "ITD": "https://www.theitdepot.com/category_filter.php/",
    "MDC": "",
}

# for ITD and any other websites that don't use straight links
site_params = {
    "ITD": {
        'filter-limit': '99999',
        # 'category': str(itd_category_dict[""]), #]),
        'filter': 'true',
    },
    "PGB": {
        'per_page': '9999',
    }
}

