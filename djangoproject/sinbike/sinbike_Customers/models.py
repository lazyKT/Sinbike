from django.db import models
from django.utils import timezone

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
    created_at = models.DateTimeField (auto_now_add=True)
    updated_at = models.DateTimeField (auto_now=True)

    class Meta:
        ordering = ['created_at']



class Transaction (models.Model):
    """
    Transaction Model
    """
    customer = models.ForeignKey (Customer, on_delete=models.CASCADE)
    amount = models.FloatField ()
    type = models.CharField (max_length=10)
    created_at = models.DateTimeField (auto_now_add = True)

    class Meta:
        ordering = ['created_at']
