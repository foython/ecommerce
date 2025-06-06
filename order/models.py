from django.db import models
from ecommerce.g_model import TimeStampMixin
from product.models import Product
from delivery.models import DeliveryType
from accounts.models import CustomUser


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


    def __str__(self):
       return f'{self.first_name} {self.last_name} {self.address} {self.city}'


options = (
    ('succeed', 'Succeed'),
    ('failed', 'Failed'),
    ('pending', 'Pending')
    )

p_type =(
    ('1', 'cash on delievery'),
    ('2', 'SSLCOMMERZ'),
      
) 

class Payment_details(TimeStampMixin):          
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='pyments')
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100, choices=p_type, default=None, blank=True, null=True)
    amount_paid = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
       return f'{self.payment_method} {self.status}'


status = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')
)


class Order(TimeStampMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment_details, on_delete=models.CASCADE, null=True, blank=True)    
    address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    delivery = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=status)
    total = models.FloatField()
    
    def __str__(self):
       return f'{self.user} {self.status}'

class OrderItem(TimeStampMixin):
    session = models.CharField(max_length=256)
    order = models.ManyToManyField(Order)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    sub_total = models.FloatField()

    def __str__(self):
       return f'{self.product} {self.size} {self.quantity} {self.sub_total}'
    

class Cupon(TimeStampMixin):
    cupon_code = models.CharField(max_length=10)
    discount_percentage = models.IntegerField()




