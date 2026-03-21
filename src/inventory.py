"""
The purpose of inventory.py module is to handle inventory management logic, including 
adding, removing, updating, and searching for inventory items. It serves as the core of the 
inventory management system, providing functions that interact with the database and 
perform necessary validations to ensure data integrity and security.
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

# A function to update an inventory item, it takes the item_id and new item data as input, validates the new data using the security module, and then calls the database function to update the corresponding record in the inventory with the new data
def update_inventory_item(item_id, name=None, price=None, quantity=None):
    # Validate item data before updating inventory
    if name is not None:
        security.validate_name(name)
    if price is not None:
        security.validate_price(price)
    if quantity is not None:
        security.validate_quantity(quantity)

    return database.update_item(item_id, {
        'name': name,
        'price': price,
        'quantity': quantity
    })

# A function to view all inventory items, it calls the database function to retrieve all items in the inventory and returns them to the caller. If there are no items, it returns a message indicating that the inventory is empty
def view_inventory():
    items = database.get_all_items()
    # If there are no items in the inventory, return a message indicating that the inventory is empty
    if not items:
        return None, "No items in inventory."
    return items, None

# A function to search for inventory items by name, it validates the input name and then calls the database function to search for items that match the given name, returning the results to the caller
def search_inventory(name):
    # Validate item name before searching inventory
    security.validate_name(name)
    return database.search_items(name)

# A function to add a vendor to an inventory item, it takes the item_id and vendor_name as input, validates the vendor name, and then calls the database function to associate the vendor with the specified inventory item
def add_vendor_to_item(item_id, vendor_name):
    # Validate vendor name before adding to item
    security.validate_name(vendor_name)
    return database.add_vendor(item_id, vendor_name)   

# A function to remove a vendor from an inventory item, it takes the item_id and vendor_name as input, validates the vendor name, and then calls the database function to remove the association between the vendor and the specified inventory item
def remove_vendor_from_item(item_id, vendor_name):
    # Validate vendor name before removing from item
    security.validate_name(vendor_name)
    return database.remove_vendor(item_id, vendor_name)

# A function to update the vendor associated with an inventory item, it takes the item_id, old_vendor_name, and new_vendor_name as input, validates the vendor names, and then calls the database function to update the vendor information for the specified inventory item
def update_vendor_for_item(item_id, old_vendor_name, new_vendor_name):
    # Validate vendor names before updating
    security.validate_name(old_vendor_name)
    security.validate_name(new_vendor_name)
    return database.update_vendor(item_id, old_vendor_name, new_vendor_name)

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

# A function to add a new category, it takes the category_name as input, validates it using the security module, and then calls the database function to add the new category to the database
def new_category(category_name):
    # Validate category name before adding to database
    security.validate_name(category_name)
    return database.add_category(category_name)

# A function to delete a category, it takes the category_name as input, validates it using the security module, and then calls the database function to delete the specified category from the database
def remove_category(category_name):
    # Validate category name before deleting from database
    security.validate_name(category_name)
    return database.delete_category(category_name)

# A function to assign a category to an inventory item, it takes the item_id and category_name as input, validates the category name using the security module, and then calls the database function to associate the specified category with the given inventory item
def get_all_categories():
    return database.get_categories()

# A function to get all items in a specific category, it takes the category_name as input, validates it using the security module, and then calls the database function to retrieve all items that belong to the specified category, returning the results to the caller
def get_all_items_by_category(category_name):
    # Validate category name before retrieving items
    security.validate_name(category_name)
    return database.get_items_by_category(category_name)

# A function to assign a category to an inventory item, it takes the item_id and category_name as input, validates the category name using the security module, and then calls the database function to associate the specified category with the given inventory item
def assign_item_to_category(item_id, category_name):    
    # Validate category name before assigning to item
    security.validate_name(category_name)
    return database.assign_category(item_id, category_name)

# A function to remove a category from an inventory item, it takes the item_id and category_name as input, validates the category name using the security module, and then calls the database function to disassociate the specified category from the given inventory item
def unassign_item_from_category(item_id, category_name):
    # Validate category name before removing from item
    security.validate_name(category_name)
    return database.unassign_category(item_id, category_name)
