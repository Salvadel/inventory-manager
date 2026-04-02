'''
database.py purpose:
Handles all interactions with the SQLite database, data access layer and handles all inventory data storage and retrieval operations.
'''
import sqlite3 # For SQLite database operations
from pathlib import Path # For handling file paths
from contextlib import contextmanager # For managing database connections
from fpdf import FPDF # For PDF export functionality

DB_NAME = Path(__file__).parent.parent / 'docs' / 'data' / 'inventory.db'

# Opens a connection, commits on success, rolls back on error, and always closes
@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# This function should be called once at startup and ensures the system has the database intact before starting operations
def init_database():
    DB_NAME.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                date_added DATE,
                date_expired DATE,
                location TEXT,
                category VARCHAR(15),
                vendor VARCHAR(20)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendors (
                vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                vendor VARCHAR(20),
                FOREIGN KEY (item_id) REFERENCES inventory(item_id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS to_buy (
                list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                FOREIGN KEY (item_id) REFERENCES inventory(item_id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                category_id INTEGER,
                FOREIGN KEY (item_id) REFERENCES inventory(item_id),
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        ''')

# A function to retrieve the user from the database and returns user records for login
def get_user(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id, username, password, salt FROM users WHERE username = ?
        ''', (username,))
        return cursor.fetchone()

# A function to add a new user to the database, it takes the username, hashed password, and salt as input, connects to the database, and inserts a new record into the users table with the provided user details
def create_user(username, hashed_password, salt):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, salt) VALUES (?, ?, ?)
        ''', (username, hashed_password.hex(), salt.hex()))

# A function to add an item to the inventory, it takes item data as input, connects to the database, and inserts a new record into the inventory table with the provided item details such as name, quantity, and price
def add_item(item_data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (name, quantity, date_added, date_expired, location, category, vendor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item_data['name'],
            item_data['quantity'],
            item_data['date_added'],
            item_data['date_expired'],
            item_data['location'],
            item_data['category'],
            item_data['vendor']
        ))

# Deletes Inventory Item from Database
def remove_item(item_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM inventory WHERE item_id = ?', (item_id,))

# A function to update an inventory item, it takes the item_id and new item data as input, connects to the database, and updates the corresponding record in the inventory table with the new data provided by the user
def update_item(item_id, item_data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE inventory SET quantity = ? WHERE item_id = ?
        ''', (item_data['quantity'], item_id))

# A function to retrieve all inventory items from the database, it connects to the database, executes a query to select all items, and returns the results
def get_all_items():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
        ''')
        return cursor.fetchall()

# A function to return matching inventory records based on the Keyword Search
def search_items(keyword):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity FROM inventory WHERE name LIKE ?
        ''', (f"%{keyword}%",))
        return cursor.fetchall()

# A function to associate a vendor with an item, updates both the vendors table and the inventory row so view_inventory reflects the change
def add_vendor(item_id, vendor):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO vendors (item_id, vendor) VALUES (?, ?)', (item_id, vendor))
        cursor.execute('UPDATE inventory SET vendor = ? WHERE item_id = ?', (vendor, item_id))

# A function to remove a vendor from an item, it deletes the record from the vendors table and resets inventory.vendor to Unknown
def remove_vendor(item_id, vendor):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM vendors WHERE item_id = ? AND vendor = ?', (item_id, vendor))
        cursor.execute('UPDATE inventory SET vendor = ? WHERE item_id = ?', ('Unknown', item_id))

# A function to update a vendor for an item, it updates the record in the vendors table and the inventory row so view_inventory reflects the change
def update_vendor(item_id, old_vendor, new_vendor):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE vendors SET vendor = ? WHERE item_id = ? AND vendor = ?
        ''', (new_vendor, item_id, old_vendor))
        cursor.execute('UPDATE inventory SET vendor = ? WHERE item_id = ?', (new_vendor, item_id))

# A function to add an item to the To-Buy list in the database, it inserts a new record into the to_buy table with the item_id of the item that needs to be purchased
def add_to_buy(item_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO to_buy (item_id) VALUES (?)', (item_id,))

# A function to remove an item from the To-Buy list in the database, it deletes the record from the to_buy table that matches the given item_id, effectively removing the item from the user's To-Buy list
def remove_from_to_buy(item_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM to_buy WHERE item_id = ?', (item_id,))

# A function to view the To-Buy list, it retrieves all items in the user's To-Buy list by joining the to_buy table with the inventory table to get the details of each item, and returns the results. If there are no items in the To-Buy list, it returns a message indicating that the list is empty
def get_to_buy_list():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT inventory.item_id, inventory.name, inventory.quantity
            FROM to_buy
            JOIN inventory ON to_buy.item_id = inventory.item_id
        ''')
        return cursor.fetchall()
    
# A function to export the To-Buy list to a PDF file, it takes a filename as input and calls the database function to retrieve the items in the To-Buy list, then formats that data into a PDF document and saves it with the given filename
def export_to_pdf(items, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="To-Buy List", ln=True, align='C')
    pdf.ln(10)
    for item in items:
        item_id, name, quantity = item
        pdf.cell(200, 10, txt=f"{item_id}: {name} (Quantity: {quantity})", ln=True)
    pdf.output(f"{filename}.pdf")

# A function to add a new category to the database, it takes the category name as input and inserts a new record into the categories table with the provided category name
def add_category(category_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))

# A function to remove a category from the database, it deletes the record from the categories table that matches the given category name
def delete_category(category_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE name = ?', (category_name,))

# A function to retrieve all categories from the database
def get_categories():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM categories')
        return cursor.fetchall()

# Looks up a category's ID by its name, returns None if not found
def get_category_id_by_name(category_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT category_id FROM categories WHERE name = ?', (category_name,))
        result = cursor.fetchone()
        return result[0] if result else None

# A function to assign an item to a category, updates both item_categories and the inventory row so view_inventory reflects the change
def assign_category(item_id, category_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO item_categories (item_id, category_id) VALUES (?, ?)', (item_id, category_id))
        cursor.execute('SELECT name FROM categories WHERE category_id = ?', (category_id,))
        category_name = cursor.fetchone()[0]
        cursor.execute('UPDATE inventory SET category = ? WHERE item_id = ?', (category_name, item_id))

# A function to remove an item from a category, deletes from item_categories and resets inventory.category to General
def unassign_category(item_id, category_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM item_categories WHERE item_id = ? AND category_id = ?', (item_id, category_id))
        cursor.execute('UPDATE inventory SET category = ? WHERE item_id = ?', ('General', item_id))

# A function to retrieve items by category, it takes the category_id as input, connects to the database, and retrieves all items that belong to the specified category by joining the inventory table with the item_categories table
def get_items_by_category(category_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT inventory.item_id, inventory.name, inventory.quantity
            FROM inventory
            JOIN item_categories ON inventory.item_id = item_categories.item_id
            WHERE item_categories.category_id = ?
        ''', (category_id,))
        return cursor.fetchall()

# SORTING ITEMS 

def sort_items_by_expiration():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            ORDER BY date_expired ASC
        ''')
        return cursor.fetchall()
    
def sort_items_by_date_added():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            ORDER BY date_added DESC
        ''')
        return cursor.fetchall()
    
def sort_items_by_name():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            ORDER BY name ASC
        ''')
        return cursor.fetchall()

def sort_items_by_quantity():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            ORDER BY quantity DESC
        ''')
        return cursor.fetchall()

def sort_items_by_location():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            ORDER BY location ASC
        ''')
        return cursor.fetchall()
    
def sort_items_by_category():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            ORDER BY category ASC
        ''')
        return cursor.fetchall()
    
def sort_items_by_vendor():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            ORDER BY vendor ASC
        ''')
        return cursor.fetchall()
    