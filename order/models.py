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
    ('0', 'Paypal'),
    ('1', 'cash on delievery'),
    ('2', 'credit card'),
    ('3', 'direct bank transfer'),    
) 

class Payment_details(TimeStampMixin):    
    amount = models.FloatField()
    payment_type = models.CharField(max_length=32, choices=p_type, default=None, blank=True, null=True)
    status = models.CharField(max_length=32, choices=options, default=None, blank=True, null=True)


    def __str__(self):
       return f'{self.payment_type} {self.status}'


status = (
    ('pending', 'Pending'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')
)


class Order(TimeStampMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment_details, on_delete=models.CASCADE)    
    address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    delivery = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=status)
    total = models.FloatField()

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




