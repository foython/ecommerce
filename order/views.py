from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BillingForm
from cart.models import Cart
from order.models import Order, OrderItem, Payment_details
from delivery.models import DeliveryType
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def confirm_order(request):    
    if request.user.is_authenticated and request.method == 'POST':
        payment_type = request.POST['paymentRadio'] 
        session_key = request.COOKIES.get('key')    
        carts = Cart.objects.filter(session=session_key)
        if carts:            
            total = Cart.objects.filter(session=request.COOKIES.get('key')).aggregate(Sum('total'))       
        
            if payment_type == '1':            
                payment_int = Payment_details.objects.create(
                    amount=total['total__sum'],
                    payment_type=int(payment_type),
                    status='pending'
                )                 
                billing_fm = BillingForm(request.POST)
                if billing_fm.is_valid():
                    billing_inst = billing_fm.save()
                    order_inst = Order.objects.create(
                        user=request.user,
                        payment = payment_int,
                        address=billing_inst,
                        delivery=DeliveryType.objects.get(pk=request.POST['deliveryid']),
                        status='pending',
                        total=total['total__sum']
                    )
                    
                    for item in carts:
                        order_item = OrderItem.objects.create(
                            session=session_key,                        
                            product=item.product,
                            size=item.size,
                            quantity=item.quantity,
                            sub_total=item.total
                        )                     
                        order_item.order.add(order_inst)
                    carts.delete()
                    response = redirect('profile')
                    response.delete_cookie('key',)
                    return response        
        else:
            return redirect('shop')
    else:
        return redirect('login')