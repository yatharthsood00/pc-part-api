import sqlite3

# helper variables (table names, etc.)
website_tables = {"theitdepot": "itd_products",
                  "mdcomputers": "md_products",
                  "primeabgb": "prime_products"
                }

database_file = 'database.db'

class DatabaseUtils:
    def __init__(self, database_file, website_name):
        self.database_file = database_file
        self.conn = self.initialise()
        self.cursor = self.conn.cursor()
        self.website = website_name
        self.table_name = website_tables[website_name]

    def initialise(self):
        conn = sqlite3.connect(self.database_file)
        return conn
    
    def create_table(self):
        # Create the table if it doesn't exist
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                link VARCHAR,
                                name TEXT(200),
                                price INTEGER,
                                instock INTEGER,
                                date DATE,
                                category text(30))
                            ;''')

    def append_data_to_table(self, data):
        # Append data to the table as a tuple: LNPIDC
        print(data)
        self.cursor.execute(f'''INSERT INTO {self.table_name} (
                                link,
                                name,
                                price,
                                instock,
                                date,
                                category
                            ) VALUES (?, ?, ?, ?, CURRENT_DATE, ?);''', data)

    def close(self):
        # Commit changes and close the connection
        self.conn.commit()
        self.conn.close()