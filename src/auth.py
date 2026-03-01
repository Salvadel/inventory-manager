"""
auth.py purpose:
Handles user authentication and login validation.

Key features:
- Validate user login
- Secure password comparison
- Generate secure tokens


def login_user(username: str, password: str) -> bool:
    input: username (str), password (str)
    output: bool
    use: Verifies user credentials against stored database record
    pass

def verify_password(password:str, stored_hash: bytes, stored_salt: bytes):
    input: password (str), stored_hash (bytes), stored_salt (bytes)
    output: bool
    use: Compares provided password with securely stored hash and salt
    pass

def hash_password(password: str) -> str:
    input: password (str)
    output: str
    use: Returns securely hashed password
    pass
"""

import hashlib
import hmac
import secrets
from security import validate_username, validate_password
from database import get_user

# Constraints:
ITERATIONS = 100000
SALT_LENGTH = 16
HASH_ALGORITHM = 'sha256'

''' This function is used the has the password using a SHA-256 algorithm with a unique salt for each password. It returns the hashed password as a hexadecimal string. '''
def hash_password(password):
    # Generates a random salt 16 bytes long
    salt = secrets.token_bytes(SALT_LENGTH) 

    # Hashes the password using PBKDF2 with SHA-256 and 100,000 iterations making brute force attacks slower
    hashed_password = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode('utf-8'), salt, ITERATIONS) 
    return hashed_password, salt

''' This function tests the provided password against the stored hash and salt. It hashes the input password using the same method and compares it to the stored hash using hmac.compare_digest for secure comparison. '''
def verify_password(password, hashed_password, salt):
    # Hashes the inputted password using the same formula and salt as the stored password
    new_hashed = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode('utf-8'), salt, ITERATIONS)
    
    # Compares the newly hashed password with the stored hash securely to prevent timing attacks
    return hmac.compare_digest(new_hashed, hashed_password) 

''' This function handles the login process by fetching the user from the database, verifying the username and password against the stored hash and salt. It returns a success status and message based on the outcome of the login attempt. '''
def login_user(username, password):
    # Fetch the user from the database
    user = get_user(username)

    # Return "User not found." If the username is not in the database
    if user is None:
        return False, 'User not found.'
    
    # Unpack the user data from the database
    _, _, stored_hash, stored_salt = user

    # Convert string back to bytes for computation
    stored_hash = bytes.fromhex(stored_hash)
    stored_salt = bytes.fromhex(stored_salt)

    # Verify the password hashes against each other
    if verify_password(password, stored_hash, stored_salt):
        return True, 'Login successful.'
    else:
        return False, 'Incorrect password.'

# Tests the Login Functionalities with a Sample User that was inserted into the database 'LabTA' with the password 'COMLab123!'
success, message = login_user("LabTA", "COMLab123!")
print(success, message)
