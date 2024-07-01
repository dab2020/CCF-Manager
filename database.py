import sqlite3
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def initialize_database():
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        date TEXT,
        address TEXT,
        parking TEXT,
        service TEXT,
        room TEXT,
        size TEXT,
        roomno TEXT,
        otherinfo TEXT,
        carpetname TEXT,
        underlay TEXT,
        gripers TEXT,
        doorbars TEXT,
        doorbartype TEXT,
        total REAL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY,
        sale_id INTEGER,
        qty INTEGER,
        desc TEXT,
        price REAL,
        total REAL,
        FOREIGN KEY(sale_id) REFERENCES sales(id)
    )
    ''')
    conn.commit()
    conn.close()

def save_sale(name, phone, date, address, parking, service, room, size, roomno, otherinfo, carpetname, underlay,
              gripers, doorbars, doorbartype, total, items):
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sales (name, phone, date, address, parking, service, room, size, roomno, otherinfo, carpetname, underlay, gripers, doorbars, doorbartype, total) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, date, address, parking, service, room, size, roomno, otherinfo, carpetname, underlay, gripers,
          doorbars, doorbartype, total))
    sale_id = cursor.lastrowid
    for item in items:
        cursor.execute('INSERT INTO invoice_items (sale_id, qty, desc, price, total) VALUES (?, ?, ?, ?, ?)',
                       (sale_id, item[0], item[1], item[2], item[3]))
    conn.commit()
    conn.close()

def get_sales():
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales')
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_invoice_items(sale_id):
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM invoice_items WHERE sale_id = ?', (sale_id,))
    items = cursor.fetchall()
    conn.close()
    return items
