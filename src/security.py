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

USER_MAX_LENGTH = 20
USER_MIN_LENGTH = 4
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64

''' A function to validate the username, make sure it fits username requirements. '''
def validate_username(username):
    if not username:
        return False, "Username cannot be empty."

    if len(username) < USER_MIN_LENGTH or len(username) > USER_MAX_LENGTH:
        return False, "Username must be between 4 and 20 characters."

    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False, "Username can only contain letters, numbers, and underscores."

    return True, "Valid username."

''' A function to validate the password, make sure it fits password complexity requirements. '''
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

print(validate_username("admin"))

print(validate_password("Admin123!"))