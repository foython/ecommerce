from django.db import models


# Create your models here.
class DeliveryType(models.Model):    
    delivery_type_name = models.CharField(max_length=32)
    delivery_price = models.FloatField()

    def __str__(self):
       return self.delivery_type_name