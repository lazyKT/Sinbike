from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic

# import rest_framework methods and functions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets

import os
import json
from datetime import datetime

from .models import Customer, Transaction, Trip
from .utils import (
    get_customer_by_email,
    get_customer_by_id,
    validate_customer_request,
    hash_password,
    cmp_hashed_password,
    get_trips_by_cust_id,
    save_image,
    get_total_ride_time,
    get_total_distances_travelled,
    get_transactions_by_customer
)
from .serializers import CustomerAvatarSerializer


# Create your views here.
@csrf_exempt
def customer_login (request):
    if request.method == 'POST':
        try:
            login_data = json.loads (request.body)
            customer = get_customer_by_email (login_data['email'])
            if customer is None:
                return HttpResponse ('Wrong Credentials', status=403)
            if not cmp_hashed_password (login_data['password'], customer.password):
                return HttpResponse ('Wrong Credentials', status=403)
            return JsonResponse ({'customer': customer()}, status=200)
        except KeyError:
            return HttpResponse ('Malformed Data', status=400)

    return HttpResponse ('Method Not Allowed', status=400)


@csrf_exempt
def change_password (request, cust_id):
    """
    Change Password
    """
    if request.method == 'PUT':
        customer = get_customer_by_id (cust_id)
        if customer is None:
            return HttpResponse ('Invalid Customer', status=404)
        try:
            json_data = json.loads (request.body)
            if not cmp_hashed_password (json_data['old_password'], customer.password):
                return HttpResponse ('Authentication Failed!', status=403)
            customer.password = hash_password (json_data['new_password'])
            customer.updated_at = datetime.now()
            customer.save ()
            return HttpResponse ('Password Has Been Changed Successfully!', status=203)
        except KeyError as ke:
            return HttpResponse (ke, status=400)

    return HttpResponse ('Method Not Allowed!', status=405)


def get_customer_trip (request, cust_id):
    """
    Get Trips By Customer ID
    """
    if request.method == 'GET':
        # print ('Customer ID', cust_id)
        customer = get_customer_by_id (cust_id)
        trips = get_trips_by_cust_id (cust_id)
        return JsonResponse ({'trips': trips}, status=200)
    else:
        return HttpResponse ('Method Not Allowed', status=400)


def customer_distances (request, cust_id):
    """
    Get Distance Travelled by Customer
    """
    if request.method == 'GET':
        customer = get_customer_by_id (cust_id)
        if customer is None:
            return HttpResponse ('Customer Not Found!', status=404)
        total_distance = get_total_distances_travelled (cust_id)
        return HttpResponse (total_distance, status=200)

    return HttpResponse ('Method Not Allowed', status=405)


def customer_ride_time (request, cust_id):
    """
    Get Total Ride Times
    """
    if request.method == 'GET':
        customer = get_customer_by_id (cust_id)
        if customer is None:
            return HttpResponse ('Customer Not Found!', status=404)
        return HttpResponse (get_total_ride_time(customer), status=200)

    return HttpResponse ('Method Not Allowed', status=405)


def customer_transaction (request, cust_id):
    """
    Get Transaction by Customer ID
    """
    if request.method == 'GET':
        customer = get_customer_by_id (cust_id)
        if customer is None:
            return HttpResponse ('Customer Not Found!', status=404)
        return JsonResponse ({'transactions' : get_transactions_by_customer(customer)}, status=200)
    return HttpResponse ('Method Not Allowed!', status=405)


@method_decorator (csrf_exempt, name='dispatch')
class CustomerListView (generic.ListView):
    """
    Customers Request:
    GET all customers || Register new customer
    """

    model = Customer

    def get (self, request, *args, **kwargs):
        """
        -> Get Customer List
        """
        customer_list = Customer.objects.all()
        return JsonResponse ({'customers': [customer() for customer in customer_list]})

    def get_queryset (self):
        """
        Get all Customers
        """
        return Customer.objects.all()

    def get_queryset (self, email):
        """
        Find Customer by Email Address
        """
        return Customer.objects.filter (email = email)

    def post (self, request, *args, **kwargs):
        """
        Register new customer
        """
        try:
            json_data = json.loads (request.body)
            print ('json data', json_data)
            if validate_customer_request (json_data) == False:
                # Invalid Request: incomplete data in request body
                return HttpResponse ("Invalid Data", status=400)
            email = json_data ['email']
            # print ('email address', email)
            if get_customer_by_email (email) is not None:
                # customer associated to the given email is already existed
                return HttpResponse ("Customer Already Existed", status=400)
            # hash password
            json_data ['password'] = hash_password (json_data['password'])
            # Create new customer
            customer = Customer.objects.create (**json_data)
            return JsonResponse ({'customer': customer()}, status=201)
        except KeyError:
            return HttpResponse ("Malformed Data")


@method_decorator (csrf_exempt, name='dispatch')
class CustomerDetailListView (generic.ListView):
    """
    Requests for single customer
    : Update/Edit, Get or Delete
    """

    model = Customer

    def get_queryset (self):
        """
        Get Customer Data by id
        """
        customer = get_object_or_404 (Customer, id = self.kwargs['id'])
        return customer


    def get (self, request, *args, **kwargs):
        """
        Get Customer Details
        """
        customer = self.get_queryset()
        return JsonResponse ({'customer': customer()}, status=200)

    def put (self, request, *args, **kwargs):
        """
        Update/Edit Customer Details
        """
        customer = self.get_queryset()
        if customer is None:
            return HttpResponse ('Customer Not Found', status=404)
        try:
            json_data = json.loads (request.body)
            customer.username = json_data['username']
            customer.email = json_data['email']
            customer.updated_at = datetime.now ()
            if 'credits' in json_data:
                customer.credits = json_data['credits']
            if 'balance' in json_data:
                customer.balance = json_data['balance']
            customer.save()
            return JsonResponse ({'customer': customer()}, status=201)
        except KeyError:
            return HttpResponse ('Invalid Data', status=400)

    def delete (self, request, *args, **kwargs):
        """
        Delete Customer Data
        """
        customer = self.get_queryset()
        customer.delete ()
        return HttpResponse (status=204)


class CustomerAvatarAPIView (APIView):
    """
    Upload/Get Customer Avatar
    """
    queryset = Customer.objects.all()
    # serializer_class = CustomerAvatarSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_customer_by_id (self, id):
        customer = get_object_or_404 (Customer, id=id)
        return customer

    def get (self, request, id, format=None):
        """
        Get Customer Avatar
        """
        customer = self.get_customer_by_id (id)
        try:
            if customer.avatar == '' or customer.avatar is None:
                return HttpResponse ('No Avatar', status=204)
            with open (customer.avatar.path, 'rb') as f:
                return HttpResponse (f.read(), content_type='image/jpeg', status=200)
        except IOError as ie:
            return HttpResponse (ie, status=500)


    def post (self, request, id, format=None):
        """
        Upload new avatar
        """
        print ('request data', request.data)
        try:
            print ('request data', request.data)
            customer = self.get_customer_by_id (id)
            image_data = request.data['avatar']
            base, extension = os.path.splitext (image_data.name)
            filename = f"cust_{customer.id}{extension}"
            avatar_location = save_image (image_data, filename)
            customer.avatar = avatar_location
            print ('avatar path', customer.avatar)
            customer.updated_at = datetime.now()
            customer.save()
            with open (avatar_location, 'rb') as f:
                return HttpResponse (f.read(), content_type='image/jpeg', status=201)
        except AttributeError:
            return HttpResponse ('Malformed Data (AttributeError)', status=400)
        except KeyError:
            return HttpResponse ('Malformed Data (KeyError)', status=400)
        except IOError as ie:
            return HttpResponse (ie, status=500)
        except Exception as e:
            print ("Image Error", e)
            return HttpResponse ('Error Saving Image', status=500)


@method_decorator (csrf_exempt, name='dispatch')
class TransactionListView (generic.ListView):
    """
    Transaction List
    """

    model = Transaction

    def get_queryset (self):
        return Transaction.objects.all()

    def get (self, request, *args, **kwargs):
        """
        Get all transactions
        """
        transactions = self.get_queryset()
        return JsonResponse ({'transactions': [t() for t in transactions]}, status=200)

    def post (self, request, *args, **kwargs):
        """
        Create new transaction
        """
        try:
            json_data = json.loads (request.body)
            customer_id = json_data ['cust_id']
            # check for valid customer
            customer = get_customer_by_id (customer_id)
            if customer is None:
                return HttpResponse ('Customer Not Found', status=404)
            json_data['customer'] = customer # add customer field to json_data dict
            del json_data ['cust_id'] # remove customer_id field from json_data dict
            transaction = Transaction.objects.create (**json_data)
            return JsonResponse ({'transaction' : transaction()}, status=201)
        except KeyError:
            return HttpResponse ('Malformed Data', status=400)


@method_decorator (csrf_exempt, name='dispatch')
class TransactionDetailListView (generic.ListView):
    """
    Requests for single transaction
    Get or Delete
    """

    model = Transaction

    def get_queryset (self):
        """
        Get Transaction by Transaction ID
        """
        transaction = get_object_or_404 (Transaction, id=self.kwargs['id'])
        return transaction

    def get (self, request, *args, **kwargs):
        """
        Get Request for single transaction
        """
        transaction = self.get_queryset()
        return JsonResponse ({'transaction': transaction()}, status=200)

    def delete (self, request, *args, **kwargs):
        """
        Delete Transaction Record
        """
        transaction = self.get_queryset()
        transaction.delete ()
        return HttpResponse (status=204)


@method_decorator (csrf_exempt, name='dispatch')
class TripListView (generic.ListView):
    """
    Get All Trips
    Create new Trip
    """

    model = Trip

    def get_queryset (self):
        return Trip.objects.all()

    def get (self, request, *args, **kwargs):
        """
        get all trips
        """
        trips = self.get_queryset()
        return JsonResponse ({'trips': [trip() for trip in trips]}, status=200)

    def post (self, request, *args, **kwargs):
        """
        create new trip
        """
        try:
            trip_data = json.loads (request.body)
            customer_id = trip_data['cust_id']
            # validate customer
            customer = get_customer_by_id (customer_id)
            if customer is None:
                return HttpResponse ('Unknown Customer', status=404)
            trip_data['customer'] = customer # add customer field to trip_data dictionary
            del trip_data['cust_id'] # remove cust_id field from trip_data dictionary
            trip = Trip.objects.create (**trip_data)
            return JsonResponse ({'trip': trip()}, status=201)
        except KeyError:
            return HttpResponse ('Malformed Data', status=400)


@method_decorator (csrf_exempt, name='dispatch')
class TripDetailListView (generic.ListView):
    """
    Single Trip
    Get Trip Details, Edit/Update, Delete
    """

    model = Trip

    def get_queryset(self):
        """
        Get Trip by Trip ID
        """
        trip = get_object_or_404 (Trip, id=self.kwargs['id'])
        return trip

    def get (self, request, *args, **kwargs):
        """
        Get request for single trip
        """
        trip = self.get_queryset()
        return JsonResponse ({'trip': trip()}, status=200)

    def put (self, request, *args, **kwargs):
        """
        Update Trip On End
        """
        try:
            end_data = json.loads (request.body)
            trip = self.get_queryset()
            trip.end_time = datetime.now()
            trip.end_point = end_data['end_point'] # update end point (lat, lng)
            trip.path = end_data ['path']
            trip.promo = end_data['promo'] # update promo amount
            trip.fare = end_data['fare'] # update fare
            trip.total = end_data['total_fare'] # update total fare
            trip.distance = end_data['distance'] # update the distance travelled
            trip.status = 'complete'
            trip.save()
            return JsonResponse ({'trip': trip()}, status=201)
        except KeyError as ke:
            return HttpResponse (ke, status=400)
        except AttributeError as ae:
            return HttpResponse (ae, status=500)
