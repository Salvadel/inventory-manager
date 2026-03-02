from database import (
    add_item,
    remove_item,
    search_items,
    add_vendor,
    add_to_buy
)
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

def add_inventory_item(item_data: dict):
    print("-----Create New Entry----- \n")
    
    item_id = input("item ID:").strip()
    name = input("Item Name:").strip()
    Vendor = input("Vendor:").strip()
    Location = input("Location:").strip()
    Category = input("Category:").strip()
    try:
        Quantity = int(input("Initial Quantity:").strip())
    except ValueError:
        print("please enter a valid integer \n")
        
    Date_added = str(input("Date Added:").strip())
    Date_expiration = str(input("Expiration Date:").strip())
    
    #connect to database
    
    conn = sqlite3.connect(inventory.db)
    cursor = conn.cursor() #won't work until real database name is used
    
    cursor.execute(
                INSERT INTO inventory(Item ID,Item Name,Item Quantity,Date added,Expiration Date,Item Location,Item category,Item Vendor)
                VALUES( , , , , , , , )
                (id, name, Quantity, Date_added, Date_expiration,Item Location, Item Category, Item Vendor ))
    conn.commit()
    
    print("Database Updated \n") #delete after gui is made. Used for testing only
    except sqlite3.IntegrityError:
    print("ERROR. Item with ID '{item_id}' already in database")
    finally:
    conn.close()
    
    
def remove_inventory_item(item_id: int):
        Remove_Item_By_Id = int(input("enter id number to be removed").strip())
        
        conn = sqlite3.connect(inventory.db)
        cursor = conn.cursor()

            # Check if the item exists before deleting
            cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = ?", (item_id,))
            if cursor.fetchone() is None:
                print(f"No item found with ID {item_id}.")
                return False

            # Delete the item
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (item_id,))
            conn.commit()
            print(f"Item with ID {item_id} successfully removed.")
            return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    conn.close() 
def search_inventory(keyword: str):
    
        Search_Id = int(input("Enter ID number you would like to search:").strip())
    
        conn = sqlite3.connect(inventory.db)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        
        if row is None:
                print(f"No item found with ID {item_id}.")
                return None
            
        result = dict(row)  # Convert Row object to a plain dictionary
            print(f"Item found: {result}")
            return result
        conn.close()
def add_To_Buy(keyword:str):
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if the item exists
            cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = ?", (item_id,))
            if cursor.fetchone() is None:
                print(f"No item found with ID {item_id}.")
                return False

            # Update the need_to_buy field
            cursor.execute(
                f"UPDATE {table_name} SET need_to_buy = ? WHERE id = ?",
                (1 if need_to_buy else 0, item_id)
            )
            conn.commit()

            status = "marked as 'Need to Buy'" if need_to_buy else "unmarked (already have it)"
            print(f"Item ID {item_id} successfully {status}.")
            return True
        conn.close()
        