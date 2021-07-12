"""
Customer URLs End Points
"""
from django.urls import path

from . import views

urlpatterns = [
    path ('', views.CustomerListView.as_view(), name='customers'),
    path ('<int:id>', views.CustomerDetail.as_view(), name='customers'),
    path ('transactions/', views.TransactionListView.as_view(), name='transactions')
]
