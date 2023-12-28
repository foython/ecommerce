from django.db import models
from product.models import Product
from ecommerce.g_model import TimeStampMixin

# Create your models here.
class Cart(TimeStampMixin):
    session = models.CharField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    total = models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.id} {self.product} {self.size} {self.quantity} {self.total}"
    

def save(self, *args, **kwargs):
   self.total = self.product.price * self.quantity
   super(Cart, self).save(*args, **kwargs)

