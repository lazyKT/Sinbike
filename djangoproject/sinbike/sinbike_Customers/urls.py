"""
Customer URLs End Points
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
# from sinbike import settings

urlpatterns = [
    path ('login/', views.customer_login), # customer login
    path ('', views.CustomerListView.as_view(), name='customers'), # customer list
    path ('<int:id>', views.CustomerDetailListView.as_view(), name='customers'), # single customer
    path ('transactions/', views.TransactionListView.as_view(), name='transactions'), # transaction list
    path ('transactions/<int:id>', views.TransactionDetailListView.as_view(), name='transactions'), # single transaction
    path ('trips/', views.TripListView.as_view(), name='trips'), # trip list
    path ('trips/<int:id>', views.TripDetailListView.as_view(), name='transactions'), # single trip details
    path ('customer_trips/<int:cust_id>', views.get_customer_trip), # Customer Trips
    path ('customer_ride_time/<int:cust_id>', views.customer_ride_time), # customer total ride minutes
    path ('customer_distances/<int:cust_id>', views.customer_distances), # customer total distance travelled
    path ('avatar/<int:id>', views.CustomerAvatarAPIView.as_view(), name='Customers') # avatar get/upload
]


urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
