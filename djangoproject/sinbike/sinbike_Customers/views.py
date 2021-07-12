from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic

import json

from .models import Customer
from .validators import get_customer_by_email, validate_customer_request


# Create your views here.
def say_hello (resquest):
    return HttpResponse ('Hello Customer')

"""
Customers Request:
GET all customers || Register new customer
"""
@method_decorator (csrf_exempt, name='dispatch')
class CustomerListView (generic.ListView):
    model = Customer
    def get (self, request, *args, **kwargs):
        """
        -> Get Customer List
        """
        customer_list = Customer.objects.all().values()
        return JsonResponse ({'customers': list(customer_list)})

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
            if validate_customer_request (json_data) == False:
                # Invalid Request: incomplete data in request body
                return HttpResponse ("Invalid Data", status=400)
            email = json_data ['email']
            print ('email address', email)
            if len (list(get_customer_by_email (email))) > 0:
                # customer associated to the given email is already existed
                return HttpResponse ("Customer Already Existed", status=401)
            # Create new customer
            customer = Customer.objects.create (**json_data)
            return JsonResponse (model_to_dict(customer), status=201)
        except KeyError:
            return HttpResponse ("Malformed Data")


"""
Requests for single customer
: Update/Edit, Get or Delete
"""
@method_decorator (csrf_exempt, name='dispatch')
class CustomerDetail (generic.ListView):
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
        customer_dict = model_to_dict(self.get_queryset())
        return JsonResponse (customer_dict)

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
            if 'credits' in json_data:
                customer.credits = json_data['credits']
            if 'balance' in json_data:
                customer.balance = json_data['balance']
            customer.save()
            return JsonResponse (model_to_dict(customer), status=203)
        except KeyError:
            return HttpResponse ('Invalid Data', status=400)

    def delete (self, request, *args, **kwargs):
        """
        Delete Customer Data
        """
        customer = self.get_queryset()
        customer.delete ()
        return HttpResponse (status=204)
