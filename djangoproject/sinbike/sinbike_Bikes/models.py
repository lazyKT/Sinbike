from django.db import models

from sinbike_Customers.models import Customer

# Create your models here.

class Bike (models.Model):
    """
    Bike Model
    """
    id = models.CharField (max_length=64, primary_key=True)
    vendor = models.CharField (max_length=128, default='others')
    reserved_by = models.ForeignKey (Customer, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField (auto_now_add=True)
    updated_at = models.DateTimeField (auto_now=True)

    def __str__ (self):
        created_at_str = (self.created_at).strftime ('%d/%m/%y %H:%M')
        return 'bike_id: %s, vendor: %s, created_at: %s' % (self.id, self.vendor, created_at_str)

    def __call__ (self):
        created_at_str = (self.created_at).strftime ('%d/%m/%y %H:%M')
        updated_at_str = (self.updated_at).strftime ('%d/%m/%y %H:%M')
        customer_id = '' if self.reserved_by is None else self.reserved_by.id
        return {
            'bike_id': self.id,
            'vendor': self.vendor,
            'reserved_by': customer_id,
            'created_at': created_at_str,
            'updated_at': updated_at_str
        }

    class Meta:
        ordering = ['created_at']


class Reservation (models.Model):
    """
    Bike Reservation
    """
    customer = models.ForeignKey (Customer, on_delete=models.CASCADE)
    bike = models.ForeignKey (Bike, on_delete=models.CASCADE)
    reserved_time = models.DateTimeField ()
    status = models.CharField (max_length=16, default='active')
    created_at = models.DateTimeField (auto_now_add=True)

    def __str__ (self):
        reserved_time_str = (self.reserved_time).strftime ('%d/%m/%y %H:%M')
        created_at_str = (self.created_at).strftime ('%d/%m/%y %H:%M')
        return 'Rerservation ID: %d, Customer ID: %d, Bike ID: %s, Time: %s, Status: %s, Created At: %s' % (self.id, self.customer.id, self.bike.id, reserved_time_str, self.status, created_at_str)

    def __call__ (self):
        reserved_time_str = (self.reserved_time).strftime ('%d/%m/%y %H:%M')
        created_at_str = (self.created_at).strftime ('%d/%m/%y %H:%M')
        return {
            'reservation_id': self.id,
            'cust_id': self.customer.id,
            'bike_id': self.bike.id,
            'status': self.status,
            'reserved_time': reserved_time_str,
            'created_at': created_at_str
        }

    class Meta:
        ordering = ['created_at']
