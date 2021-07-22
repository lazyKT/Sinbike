"""
Bikes URLs and End Points
"""
from django.urls import path

from . import views


urlpatterns = [
    path ('', views.BikeListView.as_view(), name='bikes'),
    path ('<str:id>', views.BikeDetailListView.as_view(), name='bikes'),
    path ('reservations/', views.ReservationListView.as_view(), name='reservations'),
    path ('reservations/<int:id>', views.ReservationDetailListView.as_view(), name='reservations'),
    path ('cust_reservations/<int:cust_id>', views.get_customer_reservations)
]
