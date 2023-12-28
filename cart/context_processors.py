from .models import Cart
from django.db.models import Sum


def get_cart_total(request):
    cart = Cart.objects.filter(session=request.COOKIES.get('key')).values()    
    cart_total = Cart.objects.filter(session=request.COOKIES.get('key')).aggregate(Sum('total'))    
    product_in_cart = []
    for item in cart:
        product_in_cart.append(item['product_id'])  
         
    return {'cart_total': cart_total, 'cart': Cart.objects.filter(session=request.COOKIES.get('key')), 'cart_items': product_in_cart}
