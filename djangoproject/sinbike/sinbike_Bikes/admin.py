from django.contrib import admin
from django.utils.crypto import get_random_string

from .models import Bike, Reservation

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


admin.site.register (Bike, BikeAdmin)
