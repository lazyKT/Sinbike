from django.contrib import admin

from .models import Customer, Trip, Transaction

# Register your models here.

class CustomerAdmin (admin.ModelAdmin):
    fields = ['username', 'email', 'credits', 'balance']


class TripAdmin (admin.ModelAdmin):
    fields = ['customer', 'distance', 'total']


class TransactionAdmin (admin.ModelAdmin):
    fields = ['customer', 'amount', 'type']


admin.site.register (Customer, CustomerAdmin)
admin.site.register (Trip, TripAdmin)
admin.site.register (Transaction, TransactionAdmin)
