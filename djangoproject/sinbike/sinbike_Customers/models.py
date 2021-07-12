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
    created_at = models.DateTimeField (auto_now_add = True)

    def __str__ (self):
        cust_id = self.customer.id
        return "customer_id: %s, amount: %.2f, type: %s" % (cust_id, self.amount, self.type)

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
