from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Cart
from product.models import Product

# Create your views here.

def cart(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(session= session_key)
    return render(request, 'cart.html', {'cart':cart})


def checkout(request):
    session = request.session.session_key
    return render(request, 'checkout.html')


def addtocart(request):
    if request.method == 'POST':
        data = json.loads(request.body)# dictionary
        if data is not None:
            session_key = data.get('session')
            product_id = data.get('productId')
            item_quantity = int(data.get('quantity'))
            item_size = data.get('size')            
            product = Product.objects.get(id=product_id)          
            total = product.price * item_quantity
            cart_item = Cart(session = session_key, product = product, size = item_size, quantity = item_quantity, total= total)
            cart_item.save() 
             #{pp.name: pp.id for pp in pricefilter}
            # product = list(pricefilter)
            # product = json.dumps(pricefilter)
            # print(pricefilter)
            # items = Cart.objects.filter(session=session_key).values
            # print(items)
            item ={'response': 200}
            items = json.dumps(item)
            return JsonResponse(data = items, safe = False)


def remove_cart(request, id):
    cart = Cart.objects.filter(session=request.session.session_key)
    obj = cart.get(product__id=id)
    obj.delete()
    return redirect('details', id=id)