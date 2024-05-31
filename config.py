'''Config data for the script'''

# Meta stuff, for reference
SITES = {'PGB': 'PrimeABGB', 'MDC': 'MD Computers', 'ITD': "TheITDepot"}

# database variables
WEBSITE_TABLES = {
                  "ITD": "itd_products",
                  "MDC": "mdc_products",
                  "PGB": "pgb_products",

                }

DATABASEFILE = 'database.db'

CREATE_QUERY_TEMPLATE = '''
    CREATE TABLE IF NOT EXISTS {tablename} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT(200),
        link VARCHAR,
        price INTEGER,
        instock INTEGER,
        date DATE,
        category text(30)
    );
    '''

# categories! to get through all products for itdepot. Can add categories here to get more products,
# for now only the most obvious candidates stay here

categories_master_list = [
    "Processor",
    "Cooler",
    "Motherboard",
    "Memory",
    "SSD",
    "HDD",
    "GPU",
    "Case",
    "PSU",
    "Monitor",
]

CATEGORIES = {
    "ITD": {
            "Processor": 30,
            "Cooler": 10,
            "Motherboard": 13,
            "Memory": 6,
            "SSD": 93,
            "HDD": 12,
            "GPU": 45,
            "Case": 5,
            "PSU": 14,
            "Monitor": 7,
        },
    "PGB": {
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
        },
    "MDC": {
            "Processor": "processor",
            "Cooler": "cooling-system",
            "Motherboard": "motherboards",
            "Memory": "memory",
            "SSD": "ssd-drive",
            "HDD": "internal-hdd",
            "GPU": "graphics-card",
            "Case": "cabinet",
            "PSU": "smps",
            "Monitor": "monitors",
    }
}

mdc_categories = {
    "Processor": "processor",
    "Cooler": "cooling-system",
    "Motherboard": "motherboards",
    "Memory": "memory",
    "SSD": "ssd-drive",
    "HDD": "internal-hdd",
    "GPU": "graphics-card",
    "Case": "cabinet",
    "PSU": "smps",
    "Monitor": "monitors",
}


# Crawler Variables
SITEPAGES = {
    "PGB": "https://www.primeabgb.com/buy-online-price-india/",
    "ITD": "https://www.theitdepot.com/category_filter.php/",
    "MDC": "https://mdcomputers.in/",

}

SITE_PARAMS = {
    "ITD": {
        'filter-limit': '9999',
        'category': '', #str(itd_category_dict[category])
        'filter': 'true',
    },
    "PGB": {
        'per_page': '9999',
    },
    "MDC": {
        'page': '' # replaced with in-loop page numbers
    },

}

site_product_class = {
    "PGB": "product-wrapper",
    "ITD": "product-item col-6 col-md-4 col-lg-3 p-1",
    "MDC": "right-block right-b"
}