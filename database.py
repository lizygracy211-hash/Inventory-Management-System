import sqlite3

DB_NAME = "database/inventory.db"

def connect():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Create database automatically
connect()

def add_product(product_name, category, quantity, price):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products(product_name, category, quantity, price)
    VALUES (?, ?, ?, ?)
    """, (product_name, category, quantity, price))

    conn.commit()
    conn.close()


def get_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_product(product_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))

    conn.commit()
    conn.close()

def update_product(product_id, product_name, category, quantity, price):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE products
    SET product_name=?, category=?, quantity=?, price=?
    WHERE id=?
    """, (product_name, category, quantity, price, product_id))

    conn.commit()
    conn.close()

def search_product(keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products
    WHERE product_name LIKE ? OR category LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    rows = cursor.fetchall()

    conn.close()
    return rows