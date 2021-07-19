from django.db import models
from django.utils import timezone

# from .utils import gen_avatar_upload_location

def gen_avatar_upload_location (instance: object, filename: str) -> str:
    """
    generate avatar upload location
    """
    base, extension = os.path.splitext (filename.lower()) # get uploaded file extension
    return f"avatars/cust_{instance.pk}{extension}"

# Create your models here.
class Customer (models.Model):
    """
    Customer Model
    """
    username = models.CharField (max_length=20)
    email = models.CharField (max_length=50)
    password = models.BinaryField ()
    credits = models.IntegerField (default=100)
    balance = models.FloatField (default=0)
    avatar = models.ImageField (upload_to='avatars', default='')
    created_at = models.DateTimeField (auto_now_add=True)
    updated_at = models.DateTimeField (auto_now=True)

    def __str__ (self):
        return "id: %s, name: %s" % (self.id, self.username)

    def __call__ (self):
        return {
            'id' : self.id,
            'username': self.username,
            'email': self.email,
            'credits': self.credits,
            'balance': self.balance,
            'created_at': (self.created_at).strftime("%d/%m/%y %H:%M"),
            'updated_at': (self.updated_at).strftime("%d/%m/%y %H:%M")
        }

    class Meta:
        ordering = ['created_at']



class Transaction (models.Model):
    """
    Transaction Model
    """
    customer = models.ForeignKey (Customer, on_delete=models.CASCADE)
    amount = models.FloatField ()
    type = models.CharField (max_length=10)
    created_at = models.DateTimeField (auto_now_add=True)

    def __str__ (self):
        cust_id = self.customer.id
        transaction_datetime = (self.created_at).strftime ('%d/%m/%y %H:%M')
        return "customer_id: %s, amount: %.2f, type: %s, DateTime: %s" % (cust_id, self.amount, self.type, transaction_datetime)

    def __call__ (self):
        return {
            'transaction_id': self.id,
            'customer_id': (self.customer).id,
            'amount': self.amount,
            'type': self.type,
            'created_at': (self.created_at).strftime ("%d/%m/%y %H:%M")
        }

    class Meta:
        ordering = ['created_at']


class Trip (models.Model):
    """
    Customer's Trip Model
    """
    customer = models.ForeignKey (Customer, on_delete=models.CASCADE)
    start_point = models.CharField (max_length=16)
    end_point = models.CharField (max_length=16)
    distance = models.FloatField (default=0.00)
    fare = models.FloatField (default=0.00)
    promo = models.FloatField (default=0.00)
    total = models.FloatField (default=0.00)
    start_time = models.DateTimeField (auto_now_add=True)
    end_time = models.DateTimeField (auto_now=True)


    def __str__ (self):
        trip_datetime = (self.start_time).strftime('%d/%m/%y %H:%M')
        return 'Trip ID: %d, Customer ID: %d, DateTime: %s' % (self.id, self.customer.id, trip_datetime)

    def __call__ (self):
        time_taken_seconds = (self.end_time - self.start_time).total_seconds()
        time_taken_minutes = divmod (time_taken_seconds, 60)[0]
        return {
            'trip_id': self.id,
            'customer_id': (self.customer).id,
            'start_point': self.start_point,
            'end_point': self.end_point,
            'time_taken': time_taken_minutes,
            'distance': self.distance,
            'fare': self.fare,
            'promo': self.promo,
            'total_fare': self.total
        }

    class Meta:
        ordering = ['start_time']
