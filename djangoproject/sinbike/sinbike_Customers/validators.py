"""
 The belows are to validate the Http Reqeusts and Operations on Data Models
"""
from .models import Customer


def get_customer_by_email (email):
    """
    Get Customer Data filtered by given Email Address
    """
    if email == None:
        return None
    return Customer.objects.filter (email=email)


def validate_customer_request (data):
    """
    Validate the data of new customer POST request
    """
    return 'email' in data and 'username' in data and 'password' in data
