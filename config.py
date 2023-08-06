# Meta stuff, for reference
sitenames = {'primeabgb': 'PGB', 'mdcomputers': 'MDC', 'theitdepot': 'ITD'}

# database variables
website_tables = {
                  "ITD": "itd_products",
                  "MDC": "mdc_products",
                  "PGB": "pgb_products",

                }

database_file = 'database.db'

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

itd_categories = {
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

}

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
site_pages = {
    "PGB": "https://www.primeabgb.com/buy-online-price-india/",
    "ITD": "https://www.theitdepot.com/category_filter.php/",
    "MDC": "https://mdcomputers.in/",

}

site_params = {
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

