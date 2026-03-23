"""
inventory.py purpose:
Handles inventory logic and connects GUI actions to database operations.

Key features:
- Add inventory item
- Remove inventory item
- Search inventory
- Add vendor to item
- Add item to To-Buy list


def add_inventory_item(item_data: dict) -> None:
    input: item_data (dict)
    output: None
    use: Processes and sends new item to database
    pass


def remove_inventory_item(item_id: int) -> None:
    input: item_id (int)
    output: None
    use: Removes item through database function
    pass


def search_inventory(keyword: str):
    input: keyword (str)
    output: list
    use: Returns matching items from database
    pass
"""
import database
import security


def _validate_item_id(item_id):
    if not isinstance(item_id, int) or item_id <= 0:
        raise ValueError("Item ID must be a positive integer.")

def _validate_category_name(category_name):
    if not category_name or not category_name.strip():
        raise ValueError("Category name cannot be empty.")

def _validate_vendor_name(vendor_name):
    if not vendor_name or not vendor_name.strip():
        raise ValueError("Vendor name cannot be empty.")


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
    _validate_item_id(item_id)
    return database.remove_item(item_id)

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
    _validate_category_name(category_name)
    return database.add_category(category_name)

# Validates and deletes a category by name
def delete_category(category_name):
    _validate_category_name(category_name)
    return database.delete_category(category_name)

# Resolves category name to an ID then assigns the item to that category
def assign_item_to_category(item_id, category_name):
    _validate_item_id(item_id)
    _validate_category_name(category_name)
    category_id = database.get_category_id_by_name(category_name)
    if category_id is None:
        raise ValueError(f"Category '{category_name}' not found.")
    return database.assign_category(item_id, category_id)

# Resolves category name to an ID then removes the item from that category
def unassign_item_from_category(item_id, category_name):
    _validate_item_id(item_id)
    _validate_category_name(category_name)
    category_id = database.get_category_id_by_name(category_name)
    if category_id is None:
        raise ValueError(f"Category '{category_name}' not found.")
    return database.unassign_category(item_id, category_id)

# Resolves category name to an ID then returns all items in that category
def get_all_items_by_category(category_name):
    _validate_category_name(category_name)
    category_id = database.get_category_id_by_name(category_name)
    if category_id is None:
        return []
    return database.get_items_by_category(category_id)

# Validates inputs then adds a vendor association to an item
def add_vendor_to_item(item_id, vendor_name):
    _validate_item_id(item_id)
    _validate_vendor_name(vendor_name)
    return database.add_vendor(item_id, vendor_name)

# Validates inputs then removes a vendor association from an item
def remove_vendor_from_item(item_id, vendor_name):
    _validate_item_id(item_id)
    _validate_vendor_name(vendor_name)
    return database.remove_vendor(item_id, vendor_name)

# Validates inputs then updates the vendor name on an item
def update_vendor_for_item(item_id, old_vendor_name, new_vendor_name):
    _validate_item_id(item_id)
    _validate_vendor_name(old_vendor_name)
    _validate_vendor_name(new_vendor_name)
    return database.update_vendor(item_id, old_vendor_name, new_vendor_name)

# Validates the item ID then adds it to the to-buy list
def add_item_to_buy_list(item_id):
    _validate_item_id(item_id)
    return database.add_to_buy(item_id)

# Validates the item ID then removes it from the to-buy list
def remove_item_from_to_buy_list(item_id):
    _validate_item_id(item_id)
    return database.remove_from_to_buy(item_id)

def view_to_buy_list():
    return database.get_to_buy_list()