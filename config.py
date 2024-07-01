'''Config data for the script'''

# Meta stuff, for reference
SITES = {
    'PGB': 'PrimeABGB',
    'MDC': 'MD Computers',
    'ITD': "TheITDepot",
    'PCS': 'PCStudio',
    'VDC': 'Vedant Computers',
}

# database variables
WEBSITE_TABLES = {
    "ITD": "itd_products",
    "MDC": "mdc_products",
    "PGB": "pgb_products",
    "PCS": "pcs_products",
    "VDC": "vdc_products"
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
    },
    "PCS": {
        "Processor": "processor",
        "Cooler": "cooler",
        "Motherboard": "motherboard",
        "Memory": "ram",
        "SSD": "storage?jsf=jet-woo-products-grid&tax=product_cat:360", # yeah somewhat bodged
        "HDD": "storage?jsf=jet-woo-products-grid&tax=product_cat:427", 
        "GPU": "graphics-card",
        "Case": "cabinets",
        "PSU": "power-supply",
        "Monitor": "monitor",
    },
    "VDC": {
        "Processor": "pc-components/processor",
        "Cooler": "pc-components/fans-and-cooling/cpu-cooler",
        "Motherboard": "pc-components/motherboard/",
        "Memory": "pc-components/memory",
        "SSD": "pc-components/storage/solid-state-drive",
        "HDD": "pc-components/storage/hard-disk-drive",
        "GPU": "pc-components/graphics-cards/gpu",
        "Case": "pc-components/chassis/cabinet",
        "PSU": "pc-components/power-supply-units/smps",
        "Monitor": "pc-peripherals/output-devices/monitor", # lol
    }
}


# Crawler Variables
SITEPAGES = {
    "PGB": "https://www.primeabgb.com/buy-online-price-india/",
    "ITD": "https://www.theitdepot.com/category_filter.php/",
    "MDC": "https://mdcomputers.in/",
    "PCS": "https://www.pcstudio.in/product-category/",
    "VDC": "https://www.vedantcomputers.com/"
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
    "PCS": {
        # no params required
    },
    "VDC": {
        'limit': 9999,
    }

}

PRODUCT_DIV_CLASS = {
    "PGB": "product-wrapper",
    "ITD": "product-item col-6 col-md-4 col-lg-3 p-1",
    "MDC": "right-block right-b",
    "PCS": "jet-woo-products__item jet-woo-builder-product jet-woo-thumb-with-effect",
    "VDC": "product-thumb",
}