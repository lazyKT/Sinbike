"""
 The belows functions are to validate the Http Reqeusts and Operations on Data Models
"""
import hashlib
import os

from .models import Customer, Trip
from sinbike import settings


def get_customer_by_email (email: str) -> object:
    """
    Get Customer Data filtered by given Email Address
    """
    if email == None:
        return None
    c_array = Customer.objects.filter (email=email)
    if len(c_array) < 1:
        return None
    return c_array[0]


def get_customer_by_id (id: int) -> object:
    """
    Get Customer by Customer ID
    """
    if id == None or id < 1:
        return None
    c_array = Customer.objects.filter (id=id)
    if len(c_array) < 1:
        return None
    return c_array[0]


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
    trips = Trip.objects.filter (customer=customer)
    return [trip() for trip in trips]


def get_total_distances_travelled (cust_id: int) -> int:
    """
    Compute total distance travelled by Customer
    """
    trips = get_trips_by_cust_id (cust_id)
    distances = [t['distance'] for t in trips]
    return sum(distances)


def get_total_ride_time (customer: object) -> int:
    """
    Get Total Ride Time
    """
    trips = [trip() for trip in Trip.objects.filter(customer=customer)]
    ride_minutes = [t['time_taken'] for t in trips]
    return sum(ride_minutes)


def gen_avatar_upload_location (instance: object, filename: str) -> str:
    """
    generate avatar upload location
    """
    base, extension = os.path.splitext (filename.lower()) # get uploaded file extension
    return f"avatars/cust_{instance.pk}{extension}"


def save_image (image: object, filename: str) -> str:
    """
    save image
    """
    base_path = os.path.join (settings.MEDIA_ROOT, 'avatars')
    filepath = os.path.join (base_path, filename)
    with open (filepath, 'wb+') as f:
        for chunk in image.chunks():
            f.write (chunk)
    return filepath
