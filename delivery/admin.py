from django.contrib import admin
from .models import DeliveryType

# Register your models here.
@admin.register(DeliveryType)
class DeliveryAdmin(admin.ModelAdmin):
    pass