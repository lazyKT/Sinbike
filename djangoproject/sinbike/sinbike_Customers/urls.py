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
    path ('change_password/<int:cust_id>', views.change_password), # change password
    path ('', views.CustomerListView.as_view(), name='customers'), # customer list
    path ('<int:id>', views.CustomerDetailListView.as_view(), name='customers'), # single customer
    path ('transactions/', views.TransactionListView.as_view(), name='transactions'), # transaction list
    path ('transactions/<int:id>', views.TransactionDetailListView.as_view(), name='transactions'), # single transaction
    path ('trips/', views.TripListView.as_view(), name='trips'), # trip list
    path ('trips/<int:id>', views.TripDetailListView.as_view(), name='transactions'), # single trip details
    path ('customer_trips/<int:cust_id>', views.get_customer_trip), # Customer Trips
    path ('customer_ride_time/<int:cust_id>', views.customer_ride_time), # customer total ride minutes
    path ('customer_distances/<int:cust_id>', views.customer_distances), # customer total distance travelled
    path ('customer_transactions/<int:cust_id>', views.customer_transaction), # customer transactions
    path ('avatar/<int:id>', views.CustomerAvatarAPIView.as_view(), name='Customers'), # avatar get/upload
    path ('reports/', views.ReportListView.as_view(), name='Reports'), # get all report or create report
    path ('reports/<int:id>', views.ReportDetailsListView.as_view(), name='Reports'), # get single report
    path ('reports/attachment/<int:id>', views.ReportAttachmentAPIView.as_view(), name='Attachment'), # upload report attachment
]


urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
