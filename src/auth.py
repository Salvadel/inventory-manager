import hashlib
import hmac
import secrets
from database import get_user
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


def hash_password(password: str) -> str:
    input: password (str)
    output: str
    use: Returns securely hashed password
    pass
"""
