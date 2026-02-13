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
