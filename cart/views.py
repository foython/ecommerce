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
            item ={'id': cart_item.product.id, 'quantity': cart_item.quantity, 'size': cart_item.size, 'total': cart_item.total}
            
            return JsonResponse(data = item, safe = False)


def remove_cart(request, id=None):
    if id:
        try:
            cart = Cart.objects.filter(session=request.session.session_key)
            obj = cart.get(product__id=id)
            obj.delete()
            return redirect('details', id=id)
        except:
            return redirect('details', id=id)
    else:
        cart = Cart.objects.filter(session=request.session.session_key)        
        cart.delete()
        return redirect('cart')
    

def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('productId')
        cart = Cart.objects.filter(session=request.session.session_key)
        action = data.get('action')
        if action == 'minus':
            item = cart.get(product__id = product_id)
            item.quantity = item.quantity - 1
            item.save()
            if item.quantity < 1:
                item.delete()
                item = {'id': item.product.id, 'quantity': item.quantity}           
                return JsonResponse(data = item, safe = False)
            else:                     
                item = {'id': item.product.id, 'quantity': item.quantity}           
                return JsonResponse(data = item, safe = False)
        if action == 'add':
            item = cart.get(product__id = product_id)
            item.quantity = item.quantity + 1
            item.save()          
            item = {'id': item.product.id, 'quantity': item.quantity}           
            return JsonResponse(data = item, safe = False)
            