import sqlite3

conn = sqlite3.connect('database.db')

# Customers Table
conn.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT UNIQUE,
    password TEXT
)
''')

# Bookings Table
conn.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    service_type TEXT,
    address TEXT,
    status TEXT
)
''')

# 🔹 WORKERS TABLE
conn.execute('''
CREATE TABLE IF NOT EXISTS workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    service_type TEXT NOT NULL,
    experience TEXT,
    status TEXT DEFAULT 'Pending'
)
''')


conn.commit()
conn.close()

print("Database tables created successfully!")
