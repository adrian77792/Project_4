from django.contrib import admin
from .models import Order, OrderItem
 
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
 
