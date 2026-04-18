'''
auth.py purpose:
Handles user authentication, including password hashing and verification, and user login functionality
'''
import hashlib
import hmac
import secrets
import security
import database

# Constraints:
ITERATIONS = 100000
SALT_LENGTH = 16
HASH_ALGORITHM = 'sha256'

# ---------------------------------------------------------------------------------------------------------------
# LOGIN FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------

# This function is used the has the password using a SHA-256 algorithm with a unique salt for each password. It returns the hashed password as a hexadecimal string
def hash_password(password):
    # Generates a random salt 16 bytes long
    salt = secrets.token_bytes(SALT_LENGTH) 

    # Hashes the password using PBKDF2 with SHA-256 and 100,000 iterations making brute force attacks slower
    hashed_password = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode('utf-8'), salt, ITERATIONS) 
    return hashed_password, salt

# This function tests the provided password against the stored hash and salt. It hashes the input password using the same method and compares it to the stored hash using hmac.compare_digest for secure comparison
def verify_password(password, hashed_password, salt):
    # Hashes the inputted password using the same formula and salt as the stored password
    new_hashed = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode('utf-8'), salt, ITERATIONS)
    
    # Compares the newly hashed password with the stored hash securely to prevent timing attacks
    return hmac.compare_digest(new_hashed, hashed_password) 

# This function handles the login process by fetching the user from the database, verifying the username and password against the stored hash and salt. It returns a success status and message based on the outcome of the login attempt
def login_user(username, password):
    # Fetch the user from the database
    user = database.get_user(username)

    # Return "User not found." If the username is not in the database
    if user is None:
        return False, 'User not found.'
    
    # Unpack the user data from the database
    _, _, stored_hash, stored_salt, _, _ = user

    # Convert string back to bytes for computation
    stored_hash = bytes.fromhex(stored_hash)
    stored_salt = bytes.fromhex(stored_salt)

    # Verify the password hashes against each other
    if verify_password(password, stored_hash, stored_salt):
        return True, 'Login successful.'
    else:
        return False, 'Incorrect password.'

# ---------------------------------------------------------------------------------------------------------------
# PASSWORD RESET FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------

def check_user_needs_backup(username):
    user = database.get_user(username)
    if user:
        # Index 4 is backup_hash. If it's None or empty, they need a code.
        return user[4] is None or user[4] == ""
    return False

def setup_backup_code(username, code):
    is_valid, msg = security.validate_password(code)
    if not is_valid:
        return False, msg

    hashed_code, salt = hash_password(code)
    database.set_user_backup_code(username, hashed_code, salt)
    return True, "Backup code saved."

def reset_password_with_backup(username, backup_code, new_password):
    user = database.get_user(username)
    if not user:
        return False, "User not found."
    
    # In your DB: backup_hash is index 4, backup_salt is index 5
    b_hash_hex = user[4]
    b_salt_hex = user[5]
    
    if not b_hash_hex:
        return False, "No backup code set for this account."

    b_salt = bytes.fromhex(b_salt_hex)
    b_hash = bytes.fromhex(b_hash_hex)

    # 1. Verify the backup code
    if not verify_password(backup_code, b_hash, b_salt):
        return False, "Invalid backup code."

    # 2. Validate the new password using security.py
    is_valid, msg = security.validate_password(new_password)
    if not is_valid:
        return False, msg

    # 3. Hash and save the new password
    new_hash, new_salt = hash_password(new_password)
    database.change_password(username, new_hash, new_salt)
    return True, "Password reset successfully! You can now log in."