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