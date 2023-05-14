import sqlite3
conn = sqlite3.connect('example1.db')
import  pandas  as  pd
# Load your DataFrames here
df_products = pd.read_json('actions\line_items.json', lines=True)  # lines=True is important
df_orders = pd.read_json('actions\orders.json', lines=True)
df_line_items = pd.read_json('actions\line_items.json', lines=True)



c = conn.cursor()

# Create products table
c.execute('DROP TABLE IF EXISTS products')
conn.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    permalink TEXT,
    description TEXT,
    short_description TEXT,
    price REAL,
    regular_price REAL,
    sale_price REAL,
    weight REAL,
    dimensions TEXT,
    categories TEXT,
    attributes TEXT,
    variations TEXT,
    stock_status TEXT,
    src TEXT,
    unique_categories TEXT
);
""")
# Create order table
c.execute('DROP TABLE IF EXISTS orders')
conn.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    status TEXT,
    date_created TEXT,
    currency TEXT,
    shipping_total REAL,
    total REAL,
    customer_ip_address TEXT,
    billing_state TEXT
);
""")
# Load the data from data frames into the SQLite tables*
df_products.to_sql('products', conn, if_exists='append', index=False)
df_orders.to_sql('orders', conn, if_exists='append', index=False)
df_line_items.to_sql('order_items', conn, if_exists='append', index=False)



# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
# Create table
# c.execute('''CREATE TABLE orders
 #            (order_date, order_number, order_email, color, size, status)''')

# data to be added
"""
purchases = [('2006-01-05',123456,'example@rasa.com','blue', 9, 'shipped'),
             ('2021-01-05',123457,'me@rasa.com','black', 10, 'order pending'),
             ('2021-01-05',123458,'me@gmail.com','gray', 11, 'delivered'),
            ]
"""
# add data
# c.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', purchases)

# AVAILABLE INVENTORY
# Create table
# c.execute('''CREATE TABLE inventory
#           (size, color)''')

# data to be added
""""
inventory = [(7, 'blue'),
             (8, 'blue'),
             (9, 'blue'),
             (10, 'blue'),
             (11, 'blue'),
             (12, 'blue'),
             (7, 'black'),
             (8, 'black'),
             (9, 'black'),
             (10, 'black')
            ]
"""
# add data
#c.executemany('INSERT INTO inventory VALUES (?,?)', inventory)


# Save (commit) the changes
conn.commit()

# end connection
conn.close()