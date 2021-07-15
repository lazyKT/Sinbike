"""
Customer URLs End Points
"""
from django.urls import path

from . import views

urlpatterns = [
    path ('login/', views.customer_login), # customer login
    path ('', views.CustomerListView.as_view(), name='customers'), # customer list
    path ('<int:id>', views.CustomerDetailListView.as_view(), name='customers'), # single customer
    path ('transactions/', views.TransactionListView.as_view(), name='transactions'), # transaction list
    path ('transactions/<int:id>', views.TransactionDetailListView.as_view(), name='transactions'), # single transaction
    path ('trips/', views.TripListView.as_view(), name='trips'), # trip list
    path ('trips/<int:id>', views.TripDetailListView.as_view(), name='transactions'), # single trip details
    path ('customer_trips/<int:cust_id>', views.get_customer_trip) # Customer Trips
]
