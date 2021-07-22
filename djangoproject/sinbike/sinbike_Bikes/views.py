from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views import generic

import json
import datetime

from .models import Bike, Reservation
from .utils import get_customer_by_id, get_bike_by_id


@method_decorator (csrf_exempt, name='dispatch')
class BikeListView (generic.ListView):
    """
    Get/Post Bikes
    """

    model = Bike

    def get_queryset (self):
        """ Get all Bikes """
        return Bike.objects.all()

    def get (self, request, *args, **kwargs):
        """
        Response For GET All Bikes Request
        """
        bikes = self.get_queryset()
        return JsonResponse ({'bikes': [bike() for bike in bikes]}, status=200)

    def post (self, request, *args, **kwargs):
        bike_id = f"bike_{get_random_string(8)}"
        try:
            json_data = json.loads (request.body)
            json_data['id'] = bike_id
            bike = Bike.objects.create (**json_data)
            return JsonResponse ({'bike': bike()}, status=201)
        except KeyError as ke:
            return HttpResponse (ke, status=400)
        except Exception as e:
            return HttpResponse (e, status=500)


@method_decorator (csrf_exempt, name='dispatch')
class BikeDetailListView (generic.ListView):
    """
    Get, Edit, Delete Single Bike
    """

    model = Bike

    def get_queryset (self):
        """
        get bike by id
        """
        print ('Bike ID', self.kwargs['id'])
        bike = get_object_or_404 (Bike, id=self.kwargs['id'])
        return bike

    def get (self, request, *args, **kwargs):
        """
        Bike Details for GET Request
        """
        print ('Bike ID', kwargs['id'])
        bike = self.get_queryset()
        return JsonResponse ({'bike': bike()}, status=200)

    def put (self, request, *args, **kwargs):
        """
        Edit/ Update Bike Details
        """
        bike = self.get_queryset()
        try:
            json_data = json.loads (request.body)
            bike.updated_at = datetime.datetime.now()
            bike.vendor = json_data['vendor']
            bike.save()
            # print (bike())
            return JsonResponse ({'bike': bike()}, status=200)
        except KeyError as ke:
            return HttpResponse (ke, status=400)

    def delete (self, request, *args, **kwargs):
        """
        Delete Bicycle
        """
        bike = self.get_queryset()
        bike.delete()
        return HttpResponse (status=204)


@method_decorator (csrf_exempt, name='dispatch')
class ReservationListView (generic.ListView):
    """
    Get/Post Reservations
    """

    model = Reservation

    def get_queryset (self):
        return Reservation.objects.all()

    def get (self, request, *args, **kwars):
        """
        Get All Reservations
        """
        reservations = self.get_queryset()
        return JsonResponse ({'reservations': [r() for r in reservations]}, status=200)

    def post (self, request, *args, **kwargs):
        """
        Create new reservations
        """
        try:
            json_data = json.loads (request.body)
            bike = get_bike_by_id (json_data['bike'])
            if bike is None:
                return HttpResponse ('Bike Not Found!', status=404)
            customer = get_customer_by_id (json_data['customer'])
            if customer is None:
                return HttpResponse ('Customer Not Found!', status=404)
            json_data['bike'] = bike
            json_data['customer'] = customer
            json_data['reserved_time'] = datetime.datetime.now() + datetime.timedelta(minutes=10)
            reservation = Reservation.objects.create (**json_data)
            bike.reserved_by = customer
            bike.save()
            return JsonResponse ({'reservation': reservation()}, status=201)
        except KeyError as ke:
            return HttpResponse (ke, status=400)


@method_decorator (csrf_exempt, name='dispatch')
class ReservationDetailListView (generic.ListView):
    """
    Get/Edit/Delete Single Reservation
    """

    model =Reservation

    def get_queryset (self):
        print ('id', self.kwargs['id'])
        reservation = get_object_or_404 (Reservation, id=self.kwargs['id'])
        return reservation

    def get (self, request, *args, **kwargs):
        """
        Get Reservation By Reservation ID
        """
        reservation = self.get_queryset()
        return JsonResponse ({'reservation': reservation()}, status=200)

    def put (self, request, *args, **kwargs):
        """
        Edit reservation
        """
        try:
            reservation = self.get_queryset()
            print ('reservation', reservation)
            json_data = json.loads (request.body)
            customer = get_customer_by_id (json_data['cust_id'])
            if customer is None:
                return HttpResponse ('Customer Not Found!', status=404)
            bike = get_bike_by_id (json_data['bike_id'])
            if bike is None:
                return HttpResponse ('Bike Not Found!', status=404)
            if 'status' in json_data:
                reservation.status = json_data['status']
                if json_data['status'] == 'cancel' or json_data['status'] == 'complete':
                    bike.reserved_by = None
                bike.save()
                reservation.save()
            return JsonResponse ({'reservation': reservation()}, status=200)
        except KeyError as ke:
            return HttpResponse (ke, status=400)


@csrf_exempt
def get_customer_reservations (request, cust_id):
    """
    Get Reservations By Customer ID
    """
    if request.method == 'GET':
        customer = get_customer_by_id (cust_id)
        if customer is None:
            return HttpResponse ('Customer Not Found!', status=404)
        reservations = Reservation.objects.filter(customer=customer)
        return JsonResponse ({'reservations': [r() for r in reservations]}, status=200)
