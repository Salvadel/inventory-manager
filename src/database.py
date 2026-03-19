'''
The purpose of database.py is to handle all interactions with the SQLite database, 
including initializing the database, performing operations on inventory items, managing 
vendors, and handling the To-Buy list. It serves as the data layer of the application.
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
                )
            '''
        )

        # Create Tables for Vendors        cursor.execute('''
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS vendors 
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                vendor TEXT,
                FOREIGN KEY (item_id) REFERENCES inventory(id)
                )
            '''
        )

        # Create Tables for To-Buy List
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS to_buy 
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                FOREIGN KEY (item_id) REFERENCES inventory(id)
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
        SELECT id, username, password, salt
        FROM users
        WHERE username = ?
        ''', 
        (username,)
    )

    user = cursor.fetchone()

    # Closes the Connection and Returns the User Record
    conn.close()
    return user

# A function to add an item to the inventory, it takes item data as input, connects to the database, and inserts a new record into the inventory table with the provided item details such as name, quantity, and price
def add_item(item_data):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Inserts New Inventory Items into the Database, including price, quantity, and name
    cursor.execute(
        '''
        INSERT INTO inventory (name, quantity, price)
        VALUES (?, ?, ?)
        ''', 
        (
        item_data['name'],
        item_data['quantity'],
        item_data['price']
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
        WHERE id = ?
        ''', 
        (item_id,)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to update an inventory item, it takes the item_id and new item data as input, connects to the database, and updates the corresponding record in the inventory table with the new data provided by the user
def update_item(item_id, item_data):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Updates Inventory Item in Database based on the item_id and new item data
    cursor.execute(
        '''
        UPDATE inventory
        SET name = ?, quantity = ?, price = ?
        WHERE id = ?
        ''', 
        (
        item_data['name'],
        item_data['quantity'],
        item_data['price'],
        item_id
        )
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
            SELECT id, name, quantity, price
            FROM inventory
            '''
        )
    
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results

# A function to return matching inventory records based on the Keyword Search
def search_items(keyword):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Returns Matching Inventory Records based on the Keyword Search using a LIKE query to find items that contain the keyword in their name
    cursor.execute(
        '''
        SELECT id, name, quantity, price
        FROM inventory
        WHERE name LIKE ?
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

# A function to remove a vendor from an item, it deletes the record from the vendors table that matches the given item_id and vendor name, effectively disassociating the vendor from the item
def remove_vendor(item_id, vendor):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Removes Vendor from Item by deleting the record from the vendors table that matches the given item_id and vendor name
    cursor.execute(
        '''
        DELETE FROM vendors
        WHERE item_id = ? AND vendor = ?
        ''', 
        (item_id, vendor)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to update a vendor for an item, it updates the record in the vendors table that matches the given item_id and old vendor name to the new vendor name, allowing users to change the associated vendor for an inventory item
def update_vendor(item_id, old_vendor, new_vendor):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Updates Vendor for Item by updating the record in the vendors table that matches the given item_id and old vendor name to the new vendor name
    cursor.execute(
        '''
        UPDATE vendors
        SET vendor = ?
        WHERE item_id = ? AND vendor = ?
        ''', 
        (new_vendor, item_id, old_vendor)
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

# A function to remove an item from the To-Buy list in the database, it deletes the record from the to_buy table that matches the given item_id, effectively removing the item from the user's To-Buy list
def remove_from_to_buy(item_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Removes Item from To-Buy List in Database by deleting the record from the to_buy table that matches the given item_id
    cursor.execute(
        '''
        DELETE FROM to_buy
        WHERE item_id = ?
        ''', 
        (item_id,)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to view the To-Buy list, it retrieves all items in the user's To-Buy list by joining the to_buy table with the inventory table to get the details of each item, and returns the results. If there are no items in the To-Buy list, it returns a message indicating that the list is empty
def get_to_buy_list():
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Retrieves the To-Buy List from the database by joining the to_buy table with the inventory table to get the details of each item in the To-Buy list
    cursor.execute(
        '''
        SELECT inventory.id, inventory.name, inventory.quantity, inventory.price
        FROM to_buy
        JOIN inventory ON to_buy.item_id = inventory.id
        '''
    )
    
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results

# A function to add a new category to the database, it takes the category name as input and inserts a new record into the categories table with the provided category name
def add_category(category_name):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Adds a new category to the database by inserting a new record into the categories table with the provided category name
    cursor.execute(
        '''
        INSERT INTO categories (name)
        VALUES (?)
        ''', 
        (category_name,)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to remove a category from the database, it deletes the record from the categories table that matches the given category_id, effectively removing the category from the system
def delete_category(category_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Removes a category from the database by deleting the record from the categories table that matches the given category_id
    cursor.execute(
        '''
        DELETE FROM categories
        WHERE id = ?
        ''', 
        (category_id,)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to update a category in the database, it takes the category_id and new category name as input, and updates the corresponding record in the categories table with the new category name
def get_categories():
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Retrieves all categories from the database by executing a query to select all records from the categories table
    cursor.execute(
        '''
        SELECT id, name
        FROM categories
        '''
    )
    
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results

# A function to assign an item to a category, it takes the item_id and category_id as input, connects to the database, and inserts a new record into the item_categories table linking the item_id with the category_id, effectively categorizing the inventory item under the specified category
def assign_category(item_id, category_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Assigns an item to a category by inserting a new record into the item_categories table linking the item_id with the category_id
    cursor.execute(
        '''
        INSERT INTO item_categories (item_id, category_id)
        VALUES (?, ?)
        ''', 
        (item_id, category_id)
    )

    # Save Changes to Database and Close Connection 
    conn.commit()
    conn.close()

# A function to remove an item from a category, it connects to the database and deletes the record from the item_categories table that matches the given item_id and category_id, effectively removing the association between the item and the category
def unassign_category(item_id, category_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Removes an item from a category by deleting the record from the item_categories table that matches the given item_id and category_id
    cursor.execute(
        '''
        DELETE FROM item_categories
        WHERE item_id = ? AND category_id = ?
        ''', 
        (item_id, category_id)
    )

    # Save Changes to Database and Close Connection
    conn.commit()
    conn.close()

# A function to retrieve items by category, it takes the category_id as input, connects to the database, and retrieves all items that belong to the specified category by joining the inventory table with the item_categories table
def get_items_by_category(category_id):
    # Connect to Inventory Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    # Retrieves items by category from the database by joining the inventory table with the item_categories table to get all items that belong to the specified category_id
    cursor.execute(
        '''
        SELECT inventory.id, inventory.name, inventory.quantity, inventory.price
        FROM inventory
        JOIN item_categories ON inventory.id = item_categories.item_id
        WHERE item_categories.category_id = ?
        ''', 
        (category_id,)
    )
    
    results = cursor.fetchall()

    # Save Changes to Database and Close Connection
    conn.close()
    return results
