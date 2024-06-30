# PC Price Tracker API - Script

This is a Python-based scripting system for capturing prices from several Indian storefronts that sell PC parts.

While the script can be run by anyone and you should get all parts' prices at the time of the run in the database.db SQLite file, the goal to have a contemporaneous database with historical data would remain unrealised without running the script daily.

### How to run the script:

1. Create your virtual env.
2. Run main.py.

### Current Websites Parsed:

1. [PrimeABGB](https://www.primeabgb.com)
2. [MDComputers](https://mdcomputers.in)
3. [The IT Depot](https://www.theitdepot.com/)
4. [PCStudio](https://www.pcstudio.in/)

### Future Plans:

- Must deploy for automatic database population in the future
- Several SQL-related operations on the created database e.g. Creating "current day price view" by each product (will require fuzzy matching for product names, etc.)
- Adding more websites, of course. Currently looking at bigger marketplaces
- Creating the main data retrieval API for actual use.
