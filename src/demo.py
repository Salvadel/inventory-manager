'''
This file contains the main application logic for the Inventory Management System. 
It provides a command-line interface (CLI) for users to interact with the system, 
allowing them to log in, manage inventory items, categories, vendors, and a to-buy list. 
The application is structured with a main menu that branches into submenus for different 
functionalities, such as viewing inventory, adding items, managing categories and vendors, 
and handling the to-buy list. User inputs are validated and appropriate messages are 
displayed based on the actions taken. The application relies on functions defined in the 
auth.py and inventory.py modules to perform operations related to authentication and 
inventory management.
'''
import auth
import inventory
from getpass import getpass

username = "LabTA"
password = "COMLab123!"

def clear_line():
    print("_" * 50)

def login_menu():
    while True:
        clear_line()
        print("Welcome to the Inventory Management System")
        clear_line()
        print('1. Login')
        print('2. Exit')

        # Take user input for login screen selection
        choice = input('Select an option: ')

        # If choice 1 ask for the users username and password and attempt to log in, if successful go to inventory menu, if not print error message and return to login menu
        if choice == '1':
            username = input('Username: ')
            password = getpass('Password: ')
            success, message = auth.login_user(username, password)
            print(message)
            if success:
                inventory_menu()
        # If choice 2 exit the application
        elif choice == '2':
            print('Goodbye!')
            break
        # If the user enters an invalid option print an error message and return to login menu
        else:
            print('Invalid option. Please try again.')

def inventory_menu():
    while True:
        clear_line()
        print("Inventory Management")
        clear_line()
        print('1. View Inventory')
        print('2. Add Item')
        print('3. Delete Item')
        print('4. Search Database')
        print('5. Manage Categories')
        print('6. Manage Vendors')
        print('7. To-Buy List')
        print('8. Logout')

        # Take user input for menu selection
        choice = input('Select an option: ')

        # If choice 1 print out current inventory
        if choice == '1':
            items, message = inventory.view_inventory()
            if items:
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}, Date Added: {item[3]}, Expiry: {item[4]}, Location: {item[5]}, Category: {item[6]}, Vendor: {item[7]}")
            else:
                print(message)
        # If choice 2 add a new inventory item, take in quantity, price, and name as input and validate them before adding to inventory
        elif choice == '2':
            try:
                name = input('Item Name: ')
                quantity = int(input('Quantity: '))
                date_added = input('Date Added (YYYY-MM-DD, or press Enter to skip): ').strip() or None
                date_expired = input('Expiry Date (YYYY-MM-DD, or press Enter to skip): ').strip() or None
                location = input('Location (text, or press Enter to skip): ').strip() or 'Unknown'
                category = input('Category (or press Enter to skip): ').strip() or 'General'
                vendor = input('Vendor (or press Enter to skip): ').strip() or 'Unknown'
                inventory.add_inventory_item(name, quantity, date_added, date_expired, location, category, vendor)
                print('Item added successfully.')
            except ValueError as e:
                print(f"Input Error: {e}")
        # If choice 3 delete an inventory item, take in item id as input deleting from inventory
        elif choice == '3':
            try:
                item_id = int(input('Item ID to delete: '))
                inventory.remove_inventory_item(item_id)
                print('Item deleted successfully.')
            except ValueError:
                print('Invalid ID. Please enter a number.')
        # If choice is 4 search the database for the item id and return the item
        elif choice == '4':
            keyword = input('Enter search keyword: ')
            try:
                results = inventory.search_inventory(keyword)
                if results:
                    for item in results:
                        print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
                else:
                    print('No items found matching that keyword.')
            except ValueError as e:
                print(f"Input Error: {e}")
        # If choice 5 open the category management submenu
        elif choice == '5':
            category_menu()
        # If choice 6 open the vendor management submenu
        elif choice == '6':
            vendor_menu()
        # If choice 7 open the to-buy list submenu
        elif choice == '7':
            to_buy_menu()
        # If choice 8 log out and return to login menu
        elif choice == '8':
            print('Logging out...')
            break
        # If the user enters an invalid option print an error message and return to inventory menu
        else:
            print('Invalid option. Please try again.')

def category_menu():
    while True:
        clear_line()
        print("Category Management")
        clear_line()
        print('1. View All Categories')
        print('2. Create New Category')
        print('3. Delete Category')
        print('4. Assign Item to Category')
        print('5. Unassign Item from Category')
        print('6. View Items by Category')
        print('7. Back')

        choice = input('Select an option: ')

        # View all existing categories
        if choice == '1':
            categories = inventory.get_all_categories()
            if categories:
                for category in categories:
                    print(f"- {category}")
            else:
                print('No categories found.')
        # Create a new category
        elif choice == '2':
            category_name = input('New Category Name: ')
            inventory.new_category(category_name)
            print(f"Category '{category_name}' created successfully.")
        # Delete an existing category
        elif choice == '3':
            category_name = input('Category Name to Delete: ')
            inventory.delete_category(category_name)
            print(f"Category '{category_name}' deleted successfully.")
        # Assign an item to a category
        elif choice == '4':
            try:
                item_id = int(input('Item ID: '))
                category_name = input('Category Name: ')
                inventory.assign_item_to_category(item_id, category_name)
                print(f"Item {item_id} assigned to '{category_name}' successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        # Unassign an item from a category
        elif choice == '5':
            try:
                item_id = int(input('Item ID: '))
                category_name = input('Category Name: ')
                inventory.unassign_item_from_category(item_id, category_name)
                print(f"Item {item_id} unassigned from '{category_name}' successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        # View all items belonging to a category
        elif choice == '6':
            category_name = input('Category Name: ')
            items = inventory.get_all_items_by_category(category_name)
            if items:
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
            else:
                print(f"No items found in category '{category_name}'.")
        # Return to inventory menu
        elif choice == '7':
            break
        else:
            print('Invalid option. Please try again.')

def vendor_menu():
    while True:
        clear_line()
        print("Vendor Management")
        clear_line()
        print('1. Add Vendor to Item')
        print('2. Remove Vendor from Item')
        print('3. Update Vendor for Item')
        print('4. Back')

        choice = input('Select an option: ')

        # Add a vendor to an item
        if choice == '1':
            try:
                item_id = int(input('Item ID: '))
                vendor_name = input('Vendor Name: ')
                inventory.add_vendor_to_item(item_id, vendor_name)
                print(f"Vendor '{vendor_name}' added to item {item_id} successfully.")
            except ValueError:
                print('Invalid ID. Please enter a number.')
        # Remove a vendor from an item
        elif choice == '2':
            try:
                item_id = int(input('Item ID: '))
                vendor_name = input('Vendor Name: ')
                inventory.remove_vendor_from_item(item_id, vendor_name)
                print(f"Vendor '{vendor_name}' removed from item {item_id} successfully.")
            except ValueError:
                print('Invalid ID. Please enter a number.')
        # Update a vendor for an item
        elif choice == '3':
            try:
                item_id = int(input('Item ID: '))
                old_vendor_name = input('Current Vendor Name: ')
                new_vendor_name = input('New Vendor Name: ')
                inventory.update_vendor_for_item(item_id, old_vendor_name, new_vendor_name)
                print(f"Vendor updated to '{new_vendor_name}' for item {item_id} successfully.")
            except ValueError:
                print('Invalid ID. Please enter a number.')
        # Return to inventory menu
        elif choice == '4':
            break
        else:
            print('Invalid option. Please try again.')

def to_buy_menu():
    while True:
        clear_line()
        print("To-Buy List")
        clear_line()
        print('1. View To-Buy List')
        print('2. Add Item to To-Buy List')
        print('3. Remove Item from To-Buy List')
        print('4. Back')

        choice = input('Select an option: ')

        # View all items on the to-buy list
        if choice == '1':
            items = inventory.view_to_buy_list()
            if items:
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
            else:
                print('Your to-buy list is empty.')
        # Add an item to the to-buy list
        elif choice == '2':
            try:
                item_id = int(input('Item ID to add to To-Buy List: '))
                inventory.add_item_to_buy_list(item_id)
                print(f"Item {item_id} added to To-Buy List successfully.")
            except ValueError:
                print('Invalid ID. Please enter a number.')
        # Remove an item from the to-buy list
        elif choice == '3':
            try:
                item_id = int(input('Item ID to remove from To-Buy List: '))
                inventory.remove_item_from_to_buy_list(item_id)
                print(f"Item {item_id} removed from To-Buy List successfully.")
            except ValueError:
                print('Invalid ID. Please enter a number.')
        # Return to inventory menu
        elif choice == '4':
            break
        else:
            print('Invalid option. Please try again.')

# Run the application
if __name__ == "__main__":
    inventory.startup()
    success, message = inventory.create_default_user(username, password)
    print(message)
    login_menu()