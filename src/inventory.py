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
