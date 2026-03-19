import auth
import inventory

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
            password = input('Password: ')
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
        print('4. Logout')

        # Take user input for menu selection
        choice = input('Select an option: ')

        # If choice 1 print out current inventory
        if choice == '1':
            items, message = inventory.view_inventory()
            if items:
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}, Price: ${item[3]:.2f}")
            else:
                print(message)
        # If choice 2 add a new inventory item, take in quantity, price, and name as input and validate them before adding to inventory
        elif choice == '2':
            try:
                name = input('Item Name: ')
                quantity = int(input('Quantity: '))
                price = float(input('Price: '))
                inventory.add_inventory_item(name, price, quantity)
                print('Item added successfully.')
            except ValueError as e:
                print(f"Input Error: {e}")
        # If choice 3 delete an inventory item, take in item id as input deleting from inventory
        elif choice == '3':
            item_id = int(input('Item ID to delete: '))
            inventory.remove_inventory_item(item_id)
            print('Item deleted successfully.')
        # If choice 4 log out and return to login menu
        elif choice == '4':
            print('Logging out...')
            break
        # If the user enters an invalid option print an error message and return to inventory menu
        else:
            print('Invalid option. Please try again.')

# Run the application
if __name__ == "__main__":
            inventory.startup()
            login_menu()



'''
MALCOLM

All the functiosn you use will be in inventory.py

In this section if you can add the ability to assign items to categories and view items by category that would be great. 
You can add a new menu option for managing categories in the inventory menu, allowing users to create new categories, 
assign items to categories, and view items by category. these are in:
new_category(category_name), delete_category(category_name), get_all_categories(), assign_item_to_category(item_id, category_name), 
unassign_item_from_category(item_id, category_name), and get_all_items_by_category(category_name) in inventory.py

Also if you could add the search item functionality to the inventory menu that would be great, allowing users to 
search for items by name and view the results. it is in search_inventory(name) in inventory.py

Also the ability to add and remove vendors from items would be great, allowing users to manage their vendor relationships for each inventory item.
These are in add_vendor_to_item(item_id, vendor_name), remove_vendor_from_item(item_id, vendor_name), and 
update_vendor_for_item(item_id, old_vendor_name, new_vendor_name) in inventory.py

And lastly to to buy list funcationalites which are located in add_item_to_buy_list(item_id), remove_item_from_to_buy_list(item_id), and view_to_buy_list() in inventory.py

Let me know if you have any questions, all the functions should be operationsal and completed your ojb is just to gather the user inputs and display everything in the CLI.
'''