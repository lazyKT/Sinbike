"""
Helper Functions for Bike, Reservation Models and Requests
"""
from sinbike_Customers.models import Customer
from .models import Bike

def get_customer_by_id (id:int=None) -> object:
    if id is None:
        return None
    cust_array = Customer.objects.filter (id=id)
    if len(cust_array) < 1:
        return None
    return cust_array[0]


def get_bike_by_id (id:str) -> object:
    bike_array = Bike.objects.filter (id=id)
    if len(bike_array) < 1:
        return None
    return bike_array[0]
