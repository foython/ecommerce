from django.forms import ModelForm
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'main_category', 'sub_category', 'price', 'information', 'color', 'discount', 'discount_price', 'image']
