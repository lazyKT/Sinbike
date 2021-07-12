"""
 The belows functions are to validate the Http Reqeusts and Operations on Data Models
"""
import hashlib

from .models import Customer


def get_customer_by_email (email: str) -> object:
    """
    Get Customer Data filtered by given Email Address
    """
    if email == None:
        return None
    return Customer.objects.filter (email=email)


def validate_customer_request (data: dict) -> bool:
    """
    Validate the data of new customer POST request
    """
    return 'email' in data and 'username' in data and 'password' in data


def hash_password (password : str) -> bytes:
    """
    hash password with sha256
    """
    hash = hashlib.sha256 ()
    hash.update (password.encode())
    return hash.digest() # 256-bit hash password
