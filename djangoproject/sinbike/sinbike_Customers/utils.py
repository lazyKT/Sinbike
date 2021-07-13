"""
 The belows functions are to validate the Http Reqeusts and Operations on Data Models
"""
import hashlib

from .models import Customer, Trip


def get_customer_by_email (email: str) -> object:
    """
    Get Customer Data filtered by given Email Address
    """
    if email == None:
        return None
    return Customer.objects.filter (email=email)


def get_customer_by_id (id: int) -> object:
    """
    Get Customer by Customer ID
    """
    if id == None or id < 1:
        return None
    return Customer.objects.filter (id=id)


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


def cmp_hashed_password (password1: str, password2: bytes) -> bool:
    """
    Compare Hash Passwords
    """
    hash = hashlib.sha256 ()
    hash.update (password1.encode())
    hashed_pwd = hash.digest()
    return str(hashed_pwd) == str(password2)


def get_trips_by_cust_id (cust_id: int) -> list:
    """
    Get Trips by  Customer ID
    """
    customer = get_customer_by_id (cust_id)
    trips = Trip.objects.filter (customer=customer[0])
    return [trip() for trip in trips]
