
'''
The purpose of database.py is the handles all database interactions.

Key features:
- Initialize database (init_database)
- Retrieve user (get_user)
- Add inventory item (add_item)
- Remove inventory item (remove_item)
- Search items (search_items)
- Add vendor (add_vendor)
- Add item to To-Buy list (add_to_buy)
'''

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
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users 
                (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL
                )
            '''
        )

        # Create Tables for Inventory
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS inventory 
                (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                date_added DATE NOT NULL,
                date_expired DATE,
                location INT NOT NULL,
                category VARCHAR(15) NOT NULL,
                vendor VARCHAR(20) NOT NULL
                )
            '''
        )

        # Create Tables for Vendors        cursor.execute('''
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS vendors 
                (
                vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                vendor VARCHAR(20),
                FOREIGN KEY (item_id) REFERENCES inventory(item_id)
                )
            '''
        )

        # Create Tables for To-Buy List
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS to_buy 
            (
                list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                FOREIGN KEY (item_id) REFERENCES inventory(item_id)
            )
            '''
        )

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
    cursor.execute(
        '''
        SELECT user_id, username, password, salt
        FROM users
        WHERE username = ?
        ''', 
        (username,)
    )

    user = cursor.fetchone()

    # Closes the Connection and Returns the User Record
    conn.close()
    return user

''' Inserts New Inventory Item into Database '''
def add_item(item_data):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Inserts New Inventory Items into the Database, including price, quantity, and name
    cursor.execute(
        '''
        INSERT INTO inventory (name, quantity, date_added, date_expired, location, category, vendor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', 
        (
        item_data['name'],
        item_data['quantity'],
        item_data['date_added'],
        item_data['date_expired'],
        item_data['location'],
        item_data['category'],
        item_data['vendor']
        )
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# Deletes Inventory Item from Database
def remove_item(item_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Deletes Inventory Item from Database based on the item_id
    cursor.execute(
        '''
        DELETE FROM inventory
        WHERE item_id = ?
        ''', 
        (item_id,)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to return matching inventory records based on the Keyword Search
def search_items(keyword):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Returns Matching Inventory Records based on the Keyword Search using a LIKE query to find items that contain the keyword in their name
    cursor.execute(
        '''
        SELECT item_id, name, quantity
        FROM inventory
        WHERE name inventory ?
        ''', 
        (f"%{keyword}%",)
    )
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results

# A function to associate a vendor with an item, it inserts a new record into the vendors table linking the item_id with the vendor name
def add_vendor(item_id, vendor):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Associates Vendor with Item by inserting a new record into the vendors table linking the item_id with the vendor name
    cursor.execute(
        '''
        INSERT INTO vendors (item_id, vendor)
        VALUES (?, ?)
        ''', 
        (item_id, vendor)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to add an item to the To-Buy list in the database, it inserts a new record into the to_buy table with the item_id of the item that needs to be purchased
def add_to_buy(item_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Adds Item to To-Buy List in Database by inserting a new record into the to_buy table with the item_id of the item that needs to be purchased
    cursor.execute(
        '''
        INSERT INTO to_buy (item_id)
        VALUES (?)
        ''', 
        (item_id,)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to retrieve all inventory items from the database, it connects to the database, executes a query to select all items, and returns the results
def get_all_items():
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Returns all inventory items from the database
    cursor.execute(
            '''
            SELECT item_id, name, quantity, date_added, date_expired, location, category, vendor
            FROM inventory
            '''
        )
    
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results

#Dohyeon was here