"""
database.py purpose:
Handles all database interactions.

Key features:
- Initialize database
- Retrieve user
- Add inventory item
- Remove inventory item
- Search items
- Add vendor
- Add item to To-Buy list


def init_db() -> None:
    input: None
    output: None
    use: Creates database and required tables if they do not exist
    pass


def get_user(username: str):
    input: username (str)
    output: user record
    use: Retrieves user from database
    pass


def add_item(item_data: dict) -> None:
    input: item_data (dict)
    output: None
    use: Inserts new inventory item into database
    pass


def remove_item(item_id: int) -> None:
    input: item_id (int)
    output: None
    use: Deletes inventory item from database
    pass


def search_items(keyword: str):
    input: keyword (str)
    output: list
    use: Returns matching inventory records
    pass


def add_vendor(item_id: int, vendor: str) -> None:
    input: item_id (int), vendor (str)
    output: None
    use: Associates vendor with item
    pass


def add_to_buy(item_id: int) -> None:
    input: item_id (int)
    output: None
    use: Adds item to To-Buy list in database
    pass
"""
import sqlite3
from pathlib import Path

# Constants for Database Path and Name
DB_NAME = Path(__file__).parent.parent / 'docs' / 'data' / 'inventory.db'

# This function should be called once at startup and ensures the system has the database intact before starting operations
def init_database():
    # Creates a the directory for the databae if not present
    DB_NAME.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to Inventory Database and Name inventory.db
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try: 
        # Create Tables for Users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        ''')

        # Create Tables for Inventory
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')

        # Save Changes to Database and Close Connection
        conn.commit()
    finally:
        conn.close()

# A function to retrieve the user from the database and returns user records for login
def get_user(username):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Retrieves the User from the Database and Returns User Records
    cursor.execute("""
        SELECT id, username, password, salt
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    # Closes the Connection and Returns the User Record
    conn.close()
    return user

# A function to add an inventory item, it validates the input data for name, price, and quantity using the security module before sending the item data to the database for storage nventory
def add_item(item_data):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Inserts New Inventory Items into the Database, including price, quantity, and name
    cursor.execute('''
        INSERT INTO inventory (name, quantity, price)
        VALUES (?, ?, ?)
    ''', (
        item_data['name'],
        item_data['quantity'],
        item_data['price']
    ))

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# Deletes Inventory Item from Database
def remove_item(item_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Deletes Inventory Item from Database based on the item_id
    cursor.execute('''
        DELETE FROM inventory
        WHERE id = ?
    ''', (item_id,))

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to return matching inventory records based on the Keyword Search
def search_items(keyword):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Returns Matching Inventory Records based on the Keyword Search using a LIKE query to find items that contain the keyword in their name
    cursor.execute('''
            SELECT id, name, quantity, price
            FROM inventory
            WHERE name LIKE ?
        ''', (f"%{keyword}%",))
    
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results

# A function to retrieve all inventory items from the database, it connects to the database, executes a query to select all items, and returns the results
def get_all_items():
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Returns all inventory items from the database
    cursor.execute('''
            SELECT id, name, quantity, price
            FROM inventory
        ''')
    
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results

