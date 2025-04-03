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

def get_sale_by_id(sale_id):
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales WHERE id = ?', (sale_id,))
    sale = cursor.fetchone()
    conn.close()
    return sale
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
        zipcd TEXT,
        parking TEXT,
        total REAL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY,
        sale_id INTEGER,
        type TEXT,
        desc TEXT,
        qty INTEGER,
        price REAL,
        total REAL,
        FOREIGN KEY(sale_id) REFERENCES sales(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS room_info (
        id INTEGER PRIMARY KEY,
        sale_id INTEGER,
        service_type TEXT,
        space_type TEXT,
        room_width REAL,
        room_length REAL,
        room_area REAL,
        FOREIGN KEY(sale_id) REFERENCES sales(id)
    )
    ''')
    conn.commit()
    conn.close()



def save_sale(id, name, phone, date, address, parking, total, items, zipcd, rooms):
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sales (id, name, phone, date, address, zipcd, parking, total) 
        VALUES (?,?,?,?,?,?,?,?)
    ''', (id, name, phone, date, address, zipcd, parking, total))
    sale_id = cursor.lastrowid
    for item in items:
        cursor.execute('INSERT INTO invoice_items (sale_id, type, desc, qty, price, total) VALUES (?, ?, ?, ?, ?, ?)',
                       (sale_id, item[0], item[1], item[2], item[3], item[4]))
    # Save each room entry
    for room in rooms:
        cursor.execute('''
            INSERT INTO room_info (sale_id, service_type, space_type, room_width, room_length, room_area)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sale_id, room[0], room[1], room[2], room[3], room[4]))
    conn.commit()
    conn.close()

def get_room_info(sale_id):
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT service_type, space_type, room_width, room_length, room_area 
        FROM room_info 
        WHERE sale_id = ?
    ''', (sale_id,))
    rooms = cursor.fetchall()
    conn.close()
    return rooms


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
    cursor.execute('SELECT type, desc, qty, price, total FROM invoice_items WHERE sale_id = ? ORDER BY id', (sale_id,))
    items = cursor.fetchall()
    conn.close()
    return items


def update_sale(sale_id, name, phone, date, address, parking, total, items, zipcd):
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE sales
        SET name = ?, phone = ?, date = ?, address = ?, parking = ?, total = ?, zipcd = ?
        WHERE id = ?
    ''', (name, phone, date, address, parking, total, zipcd, sale_id))

    # Delete existing items
    cursor.execute('DELETE FROM invoice_items WHERE sale_id = ?', (sale_id,))

    # Insert new/updated items
    for item in items:
        cursor.execute('INSERT INTO invoice_items (sale_id, type, desc, qty, price, total) VALUES (?, ?, ?, ?, ?, ?)',
                       (sale_id, item[0], item[1], item[2], item[3], item[4]))

    conn.commit()
    conn.close()