import datetime
from django.contrib import admin
from django.utils.crypto import get_random_string

from .models import Bike, Reservation
from sinbike_Customers.models import Customer

# Register your models here.

class BikeAdmin (admin.ModelAdmin):
    fields = ['vendor']
    actions = ['delete_model', 'delete_queryset']

    def save_model (self, request, obj, form, change):
        if not change:
            obj.id = f"bike_{get_random_string(8)}"
        super().save_model (request, obj, form, change)
        # print (obj, request, form)

    def delete_model (self, request, obj):
        print ('========== delete_model ===========')
        print ('Deleting Single Model from Admin Panel!!')
        obj.delete()

    def delete_queryset (self, request, queryset):
        print ('========== delete_queryset ===========')
        print ('Bulk Delete')
        queryset.delete()



class ReservationAdmin (admin.ModelAdmin):
    fields = ['customer', 'bike']
    actions = ['delete_model', 'delete_many']

    def save_model (self, request, obj, form, change):
        if not change:
            obj.reserved_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
        super().save_model (request, obj, form, change)

    def delete_model (self, request, obj):
        obj.delete()

    def delete_many (self, request, queryset):
        queryset.delete()



admin.site.register (Bike, BikeAdmin)
admin.site.register (Reservation, ReservationAdmin)
