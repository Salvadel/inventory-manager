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
#from database import get_user

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

''' Temporary Test with mock data until database integration is complete '''
# Setup mock password hash for testing
hashed_password, salt = hash_password("admin123")

# Setup mock user data for testing
mock_user = {
    "username": "admin",
    "password_hash": hashed_password,
    "salt": salt
}

# Test with correct password
print(verify_password("admin123", mock_user["password_hash"], mock_user["salt"]))

# Test with wrong password
print(verify_password("wrongpassword", mock_user["password_hash"], mock_user["salt"]))