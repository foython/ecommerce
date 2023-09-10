from django.db import models
from ecommerce.g_model import TimeStampMixin
from product.models import Product

# Create your models here.
class BillingAddress(TimeStampMixin):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    postcode = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    phone_no = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)

class OrderItem(TimeStampMixin):
    session = models.CharField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    total = models.FloatField()


class Order(TimeStampMixin):   
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)

