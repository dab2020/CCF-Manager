# update_db.py
import sqlite3
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def update_database():
    db_path = resource_path('sales.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Check if the "rooms" table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rooms'")
    if cursor.fetchone() is None:
        cursor.execute('''
            CREATE TABLE rooms (
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
        print("Created 'rooms' table in the database.")
    else:
        print("'rooms' table already exists.")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_database()
