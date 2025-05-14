from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class MainCategory(TimeStampedModel):
    name = models.CharField(max_length=128, unique=False)

    def __str__(self):
        return self.name


class SubCategory(TimeStampedModel):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='sub_cat')
    name = models.CharField(max_length=128, unique=False)

    def __str__(self):
        return f'{self.name}'


class Product(TimeStampedModel):
    name = models.CharField(max_length=256)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, unique=False)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, unique=False)
    price = models.FloatField()
    information = models.TextField(max_length=500)
    color = models.CharField(max_length=50)
    discount = models.BooleanField(default=False)
    discount_percentage = models.FloatField(blank=True, null=True, help_text="Enter discount percentage, e.g., 20 for 20%")
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.discount and self.discount_percentage:
            self.discount_price = round(self.price * (1 - self.discount_percentage / 100), 2)
        else:
            self.discount_price = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} {self.name} {self.main_category} {self.price}"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='multi_images')
    images = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product.name

    def first_image(self):
        return self.images[0]


class SizeandQuantity(models.Model):
    SIZE_CHOICES = (
        ('32', '32'),
        ('34', '34'),
        ('36', '36'),
        ('38', '38'),
        ('40', '40'),
        ('S', 'short'),
        ('M', 'medium'),
        ('L', 'large'),
        ('XL', 'extra large'),
        ('XXL', 'extra x large'),

    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZE_CHOICES, max_length=30)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.product.name