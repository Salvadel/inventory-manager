"""
security.py purpose:
Handles input validation and security checks.

Key features:
- Validate usernames
- Validate passwords
- Enforce security rules


def validate_username(username: str) -> bool:
    input: username (str)
    output: bool
    use: Ensures username meets security requirements
    pass


def validate_password(password: str) -> bool:
    input: password (str)
    output: bool
    use: Ensures password meets strength requirements
    pass
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

# For reference security.py should be used wehen adding a new user or passwordto ensure they meet security requirements.