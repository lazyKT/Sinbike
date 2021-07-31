from django.contrib import admin

from .models import Customer, Trip, Transaction

# Register your models here.

class CustomerAdmin (admin.ModelAdmin):
    fields = ['username', 'email', 'credits', 'balance']

    actions = ['delete_model', 'delete_queryset']

    def delete_model (self, request, obj):
        print ('========== delete_model ===========')
        print ('Deleting Single Model from Admin Panel!!')
        obj.delete()

    def delete_queryset (self, request, queryset):
        print ('========== delete_queryset ===========')
        print ('Bulk Delete')
        queryset.delete()


class TripAdmin (admin.ModelAdmin):
    fields = ['customer', 'start_point', 'end_point', 'path' , 'status', 'distance', 'fare', 'promo', 'total']

    actions = ['delete_model', 'delete_queryset']

    def delete_model (self, request, obj):
        print ('========== delete_model ===========')
        print ('Deleting Single Model from Admin Panel!!')
        obj.delete()

    def delete_queryset (self, request, queryset):
        print ('========== delete_queryset ===========')
        print ('Bulk Delete')
        queryset.delete()


class TransactionAdmin (admin.ModelAdmin):
    fields = ['customer', 'amount', 'type']

    actions = ['delete_model', 'delete_queryset']

    def delete_model (self, request, obj):
        print ('========== delete_model ===========')
        print ('Deleting Single Model from Admin Panel!!')
        obj.delete()

    def delete_queryset (self, request, queryset):
        print ('========== delete_queryset ===========')
        print ('Bulk Delete')
        queryset.delete()


admin.site.register (Customer, CustomerAdmin)
admin.site.register (Trip, TripAdmin)
admin.site.register (Transaction, TransactionAdmin)
