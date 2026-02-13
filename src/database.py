import sqlite3
from pathlib import Path
"""
database.py purpose:
Handles all database interactions.

Key features:
- Initialize database
- Retrieve user
- Add inventory item
- Remove inventory item
- Search items
- Add vendor
- Add item to To-Buy list


def init_db() -> None:
    input: None
    output: None
    use: Creates database and required tables if they do not exist
    pass


def get_user(username: str):
    input: username (str)
    output: user record
    use: Retrieves user from database
    pass


def add_item(item_data: dict) -> None:
    input: item_data (dict)
    output: None
    use: Inserts new inventory item into database
    pass


def remove_item(item_id: int) -> None:
    input: item_id (int)
    output: None
    use: Deletes inventory item from database
    pass


def search_items(keyword: str):
    input: keyword (str)
    output: list
    use: Returns matching inventory records
    pass


def add_vendor(item_id: int, vendor: str) -> None:
    input: item_id (int), vendor (str)
    output: None
    use: Associates vendor with item
    pass


def add_to_buy(item_id: int) -> None:
    input: item_id (int)
    output: None
    use: Adds item to To-Buy list in database
    pass
"""
