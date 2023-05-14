import sqlite3
conn = sqlite3.connect('example1.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE orders
#              (text, trans text, symbol text, qty real, price real)''')


# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
c.execute('DROP TABLE IF EXISTS dummy')
# Create table
c.execute('''CREATE TABLE dummy (
    id INTEGER PRIMARY KEY,
    order_name TEXT,
    order_email TEXT,
    order_address TEXT,
    order_phone TEXT,
    order_quantity INTEGER,
    order_product TEXT
);''')

c.execute('DROP TABLE IF EXISTS orders')

c.execute('''CREATE TABLE orders
             (order_date, order_number, order_email, color, size, status)''')

# data to be added
purchases = [('2006-01-05',123456,'example@rasa.com','blue', 9, 'shipped'),
             ('2021-01-05',123457,'me@rasa.com','black', 10, 'order pending'),
             ('2021-01-05',123458,'me@gmail.com','gray', 11, 'delivered'),
            ]

orderss = [('1','mounir','mounir@rasa.com','Av. Taieb Mhiri Hammamet 8050','56789412','5','baklawa'),
           ('2','salah','salah@gmail.com','Ariana','54123698','3','kaak' )]

# add data
c.executemany('INSERT INTO dummy VALUES (?,?,?,?,?,?,?)', orderss)

# add data
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', purchases)

# AVAILABLE INVENTORY
c.execute('DROP TABLE IF EXISTS inventory')
# Create table
c.execute('''CREATE TABLE inventory
             (size, color)''')

# data to be added
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

# add data
c.executemany('INSERT INTO inventory VALUES (?,?)', inventory)


# Save (commit) the changes
conn.commit()

# end connection
conn.close()