from django.db import models

# Create your models here.
class Customer (models.Model):
    """
    Customer Model
    """
    username = models.CharField (max_length=20)
    email = models.CharField (max_length=50)
    password = models.CharField (max_length=30)
    credits = models.IntegerField (default=100)
    balance = models.FloatField (default=0)


class Transaction (models.Model):
    """
    Test Model
    """
    amount = models.FloatField ()
    type = models.CharField (max_length=10)
