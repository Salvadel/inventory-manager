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

# A function to initialize the application, setting up database connections and any necessary configurations. This is called at the start of the application to ensure everything is ready for use
def startup():
    database.init_database()

#A function to add an inventory item, it validates the input data for name, price, and quantity using the security module before sending the item data to the database for storage. It ensures that only valid data is added to the inventory.
def add_inventory_item(name, price, quantity):
    # Validate item data before adding to inventory
    security.validate_name(name)
    security.validate_price(price)
    security.validate_quantity(quantity)

    return database.add_item({
        'name': name,
        'price': price,
        'quantity': quantity
    })

# A function to remove an inventory item, it takes the item_id as input and calls the database function to remove the item from the inventory
def remove_inventory_item(item_id):
    return database.remove_item(item_id)

# A function to search for inventory items by name, it validates the input name and then calls the database function to search for items that match the given name, returning the results to the caller
def search_inventory(name):
    # Validate item name before searching inventory
    security.validate_name(name)
    return database.search_items(name)

# A function to view all inventory items, it calls the database function to retrieve all items in the inventory and returns them to the caller. If there are no items, it returns a message indicating that the inventory is empty
def view_inventory():
    items = database.get_all_items()
    # If there are no items in the inventory, return a message indicating that the inventory is empty
    if not items:
        return None, "No items in inventory."
    return items, None

# A function to add a vendor to an inventory item, it takes the item_id and vendor_name as input, validates the vendor name, and then calls the database function to associate the vendor with the specified inventory item
def add_vendor_to_item(item_id, vendor_name):
    # Validate vendor name before adding to item
    security.validate_name(vendor_name)
    return database.add_vendor(item_id, vendor_name)   

# A function to add an item to the To-Buy list, it takes the item_id as input and calls the database function to add the specified item to the user's To-Buy list
def add_item_to_buy_list(item_id):
    return database.add_to_buy(item_id)

# A function to remove an item from the To-Buy list, it takes the item_id as input and calls the database function to remove the specified item from the user's To-Buy list
def remove_item_from_to_buy_list(item_id):
    return database.remove_from_to_buy(item_id)

# A function to view the To-Buy list, it calls the database function to retrieve all items in the user's To-Buy list and returns them to the caller. If there are no items in the To-Buy list, it returns a message indicating that the list is empty
def view_to_buy_list():
    items = database.get_to_buy_list()
    # If there are no items in the To-Buy list, return a message indicating that the list is empty
    if not items:
        return None, "To-Buy list is empty."
    return items, None
