"""
security.py purpose:
Handles security-related functions such as password validation and user creation.
"""
import re

# Constraints
USER_MAX_LENGTH = 20
USER_MIN_LENGTH = 4
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64

# A function to validate the password, make sure it fits password complexity requirements
def validate_password(password):
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > PASSWORD_MAX_LENGTH:
        return False, "Your password is too long, it must be less than 64 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*()_\-+=~`\[\]{}|;:'\",.<>?/\\]", password):
        return False, "Password must contain at least one special character."

    return True, "Valid password."

# A function to validate item names for database operations
def validate_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Item name must be a non-empty string.")

# A function to validate item price for database operations
def validate_price(price):
    if not isinstance(price, (int, float)):
        raise ValueError("Price must be a number.")
    if price <= 0:
        raise ValueError("Price must be greater than 0.")

# A function to validate item quantity for database operations
def validate_quantity(quantity):
    if not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer.")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

<<<<<<< HEAD
# For reference security.py should be used wehen adding a new user or passwordto ensure they meet security requirements.

=======
# A function to validate item IDs for database operations
def validate_item_id(item_id):
    if not isinstance(item_id, int) or item_id <= 0:
        raise ValueError("Item ID must be a positive integer.")

# A function to validate category names for database operations
def validate_category_name(category_name):
    if not category_name or not category_name.strip():
        raise ValueError("Category name cannot be empty.")

# A function to validate vendor names for database operations
def validate_vendor_name(vendor_name):
    if not vendor_name or not vendor_name.strip():
        raise ValueError("Vendor name cannot be empty.")

# A function to validate location names for database operations
def validate_location(location):
    if not location or not location.strip():
        raise ValueError("Location cannot be empty.")

# A function to validate dates for database operations
def validate_date(date_str):
    if not date_str or not date_str.strip():
        raise ValueError("Date cannot be empty.")
    # Additional date format validation can be added here if needed
    try:
        from datetime import datetime
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

# A function to validate usernames for user creation
def validate_filename(filename):
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty.")
    # Additional filename validation can be added here if needed
    if re.search(r'[<>:"/\\|?*]', filename):
        raise ValueError("Filename contains invalid characters. Avoid using <>:\"/\\|?*.")
>>>>>>> d79dc38f0c7db150d55eaf5d5ff2f4a475326d64
