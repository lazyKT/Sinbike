"""
Customer URLs End Points
"""
from django.urls import path

from . import views

urlpatterns = [
    path ('', views.CustomerListView.as_view(), name='customers'), # customer list
    path ('<int:id>', views.CustomerDetailListView.as_view(), name='customers'), # single customer
    path ('transactions/', views.TransactionListView.as_view(), name='transactions'), # transaction list
    path ('transactions/<int:id>', views.TransactionDetailListView.as_view(), name='transactions') # single transaction
]
