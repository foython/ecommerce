from django.contrib import admin
from .models import Order, OrderItem, BillingAddress, Payment_details

# Register your models here.
@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(BillingAddress)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment_details)
class ProductAdmin(admin.ModelAdmin):
    pass