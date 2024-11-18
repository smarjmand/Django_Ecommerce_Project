from django.contrib import admin
from .models import Address, Order, OrderItem

#------------------------------------------------------------------
# Register models in Django-Admin :
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)