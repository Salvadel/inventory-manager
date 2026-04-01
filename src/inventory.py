"""
inventory.py purpose:
Handles inventory management functions and validates data, acting as a seperating layer between the database and the user interface.
"""
import database
import security


# A function to initialize the application, setting up database connections and any necessary configurations. This is called at the start of the application to ensure everything is ready for use
def startup():
    database.init_database()

# Hashes the password and stores the new user in the database, skips if the user already exists
def create_default_user(username, password):
    import auth
    hashed_password, salt = auth.hash_password(password)
    try:
        database.create_user(username, hashed_password, salt)
        return True, "User created!"
    except Exception:
        return False, "User already exists."

# A function to add an inventory item, it validates the input data for name, price, and quantity using the security module before sending the item data to the database for storage. It ensures that only valid data is added to the inventory.
def add_inventory_item(name, quantity, date_added=None, date_expired=None, location='Unknown', category='General', vendor='Unknown'):
    security.validate_name(name)
    security.validate_quantity(quantity)
    return database.add_item({
        'name': name,
        'quantity': quantity,
        'date_added': date_added,
        'date_expired': date_expired,
        'location': location,
        'category': category,
        'vendor': vendor
    })

# A function to remove an inventory item, it takes the item_id as input and calls the database function to remove the item from the inventory
def remove_inventory_item(item_id):
    security.validate_item_id(item_id)
    return database.remove_item(item_id)

# Function to update an inventory item, it validates the input data for name, price, and quantity using the security module before sending the updated item data to the database for storage. It ensures that only valid data is used to update the inventory.
def update_inventory_item(item_id, name=None, quantity=None, date_added=None, date_expired=None, location=None, category=None, vendor=None):
    security.validate_item_id(item_id)
    if name is not None:
        security.validate_name(name)
    if quantity is not None:
        security.validate_quantity(quantity)
    return database.update_item(item_id, {
        'name': name,
        'quantity': quantity,
        'date_added': date_added,
        'date_expired': date_expired,
        'location': location,
        'category': category,
        'vendor': vendor
    })

# A function to search for inventory items by name, it validates the input name and then calls the database function to search for items that match the given name, returning the results to the caller
def search_inventory(name):
    security.validate_name(name)
    return database.search_items(name)

# A function to view all inventory items, it calls the database function to retrieve all items in the inventory and returns them to the caller. If there are no items, it returns a message indicating that the inventory is empty
def view_inventory():
    items = database.get_all_items()
    if not items:
        return None, "No items in inventory."
    return items, None

# Returns a flat list of all category name strings
def get_all_categories():
    results = database.get_categories()
    return [row[0] for row in results]

# Validates and creates a new category
def new_category(category_name):
    security.validate_category_name(category_name)
    return database.add_category(category_name)

# Validates and deletes a category by name
def delete_category(category_name):
    security.validate_category_name(category_name)
    return database.delete_category(category_name)

# Resolves category name to an ID then assigns the item to that category
def assign_item_to_category(item_id, category_name):
    security.validate_item_id(item_id)
    security.validate_category_name(category_name)
    category_id = database.get_category_id_by_name(category_name)
    if category_id is None:
        raise ValueError(f"Category '{category_name}' not found.")
    return database.assign_category(item_id, category_id)

# Resolves category name to an ID then removes the item from that category
def unassign_item_from_category(item_id, category_name):
    security.validate_item_id(item_id)
    security.validate_category_name(category_name)
    category_id = database.get_category_id_by_name(category_name)
    if category_id is None:
        raise ValueError(f"Category '{category_name}' not found.")
    return database.unassign_category(item_id, category_id)

# Resolves category name to an ID then returns all items in that category
def get_all_items_by_category(category_name):
    security.validate_category_name(category_name)
    category_id = database.get_category_id_by_name(category_name)
    if category_id is None:
        return []
    return database.get_items_by_category(category_id)

# Validates inputs then adds a vendor association to an item
def add_vendor_to_item(item_id, vendor_name):
    security.validate_item_id(item_id)
    security.validate_vendor_name(vendor_name)
    return database.add_vendor(item_id, vendor_name)

# Validates inputs then removes a vendor association from an item
def remove_vendor_from_item(item_id, vendor_name):
    security.validate_item_id(item_id)
    security.validate_vendor_name(vendor_name)
    return database.remove_vendor(item_id, vendor_name)

# Validates inputs then updates the vendor name on an item
def update_vendor_for_item(item_id, old_vendor_name, new_vendor_name):
    security.validate_item_id(item_id)
    security.validate_vendor_name(old_vendor_name)
    security.validate_vendor_name(new_vendor_name)
    return database.update_vendor(item_id, old_vendor_name, new_vendor_name)

# Validates the item ID then adds it to the to-buy list
def add_item_to_buy_list(item_id):
    security.validate_item_id(item_id)
    return database.add_to_buy(item_id)

# Validates the item ID then removes it from the to-buy list
def remove_item_from_to_buy_list(item_id):
    security.validate_item_id(item_id)
    return database.remove_from_to_buy(item_id)

# Returns a list of items currently in the to-buy list, or an empty list if there are none
def view_to_buy_list():
    return database.get_to_buy_list()

# A function to export the to-buy list to a PDF file, it takes a filename as input and calls the database function to retrieve the items in the to-buy list, then formats that data into a PDF document and saves it with the given filename
def export_to_buy_list(filename):
    items = database.get_to_buy_list()
    if not items:
        return False, "To-Buy List is empty."
    return database.export_to_pdf(items, filename)