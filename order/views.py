from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse,  HttpResponseRedirect, JsonResponse
from django.urls import reverse
from order.forms import BillingForm
from order.forms import BillingForm
from cart.models import Cart
from order.models import Order, OrderItem, Payment_details
from delivery.models import DeliveryType
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from product.models import SizeandQuantity
from .utils import send_order_confirmation_email
from sslcommerz_python_api import SSLCSession
from django.conf import settings
from decimal import Decimal
user = ''

# Create your views here.
@login_required(login_url='login')
def confirm_order(request):    
    if request.user.is_authenticated and request.method == 'POST':
        
        payment_type = request.POST['paymentRadio'] 
        session_key = request.COOKIES.get('key')    
        carts = Cart.objects.filter(session=session_key)
        if carts:            
            total = Cart.objects.filter(session=request.COOKIES.get('key')).aggregate(Sum('total'))       
    
            try:        
                                 
                billing_fm = BillingForm(request.POST)
                if billing_fm.is_valid():
                    billing_inst = billing_fm.save()
                    if payment_type == '1': 
                        payment_int = Payment_details.objects.create(
                        user = request.user,                   
                        payment_method=int(payment_type),
                        amount_paid=total['total__sum'],
                        status='pending'
                        )
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
                            product = SizeandQuantity.objects.filter(product__id=item.product.id, size=item.size).last()
                            print(product)
                            product.quantity -= item.quantity
                            product.save()
                        
                        carts.delete()                        
                        response = redirect('profile')
                        response.delete_cookie('key',)                                   
                        return response
                    
                    elif payment_type == '2':
                        order_inst = Order.objects.create(
                            user=request.user,
                            # payment = payment_int,
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
                            product = SizeandQuantity.objects.filter(product__id=item.product.id, size=item.size).last()
                            print(product)
                            product.quantity -= item.quantity
                            product.save()                         
                        return redirect('payment')
                  
            except Exception as e:
                return HttpResponse('Error Occurred: ' + str(e))
                   
                        
        else:
            return redirect('shop')
    else:        
        return redirect('login')
    
    
    
@login_required
def payment(request):
    mypayment = SSLCSession(
        sslc_is_sandbox=True,
        sslc_store_id=settings.SSLCOMMERZ_STORE_ID,
        sslc_store_pass=settings.SSLCOMMERZ_STORE_PASS,
    )

    status_url = request.build_absolute_uri("payment_status/")

    mypayment.set_urls(
        success_url=status_url,
        fail_url=status_url,
        cancel_url=status_url,
        ipn_url=status_url,
    )
    global user
    user = request.user
    order = Order.objects.filter(user=user).last()

    mypayment.set_product_integration(
        total_amount=Decimal(order.total),
        currency="BDT",
        product_category="clothing",
        product_name="demo-product",
        num_of_item=2,
        shipping_method="YES",
        product_profile="None",
    )

    mypayment.set_customer_info(
        name=user.first_name,
        email=user.email,
        address1=order.address.address,
        address2='Bangladesh',
        city=order.address.city, 
        postcode=order.address.postcode,       
        country=order.address.country,
        phone=order.address.phone_no,
    )

    mypayment.set_shipping_info(
        shipping_to=user.first_name,
        address=order.address,
        city=order.address.city,
        postcode=order.address.postcode,
        country=order.address.country,
    )
    
    response_data = mypayment.init_payment()
    
    
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def payment_status(request):
    if request.method == "POST":
        payment_data = request.POST
        if payment_data.get("status") == "VALID":
            val_id = payment_data.get("val_id")
            tran_id = payment_data.get("tran_id")
                                    
            # Use session to get order if user is anonymous
            return HttpResponseRedirect(
                reverse("sslc_complete", kwargs={"val_id": val_id, "tran_id": tran_id})
            )
        else:
            return JsonResponse({"status": "error", "message": "Payment failed"})

    return render(request, "orders/status.html")



def sslc_complete(request, val_id, tran_id):
    try:           
        order = Order.objects.filter(user=user).last()
        # user = request.user  
        session_key = request.COOKIES.get('key')              

        if not order:
            return HttpResponse({"status": "error", "message": "Order not found"})

        payment = Payment_details.objects.create(
            user=user,
            payment_id=val_id,
            payment_method=2,
            amount_paid=order.total,
            status="Completed",
        )

        order.status = "completed"
        order.payment = payment
        order.save()
        
        # Delete cart
        Cart.objects.filter(session=session_key).delete()

        context = {
            "order": order,
            "transaction_id": tran_id,
        }
        return render(request, "orders/status.html", context)
    
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

    # else:
    #     return HttpResponse({"status": "error", "message": "Payment failed"})

    # return render(request, "orders/status.html")


# @csrf_exempt
# def payment_status(request):
#     if request.method == "POST":
#         payment_data = request.POST
#         if payment_data["status"] == "VALID":
#             val_id = payment_data["val_id"]
#             tran_id = payment_data["tran_id"]
#             user=request.user
#             order = Order.objects.filter(user=user).last()

#             payment = Payment_details.objects.create(
#                 user=user,
#                 payment_id=val_id,
#                 payment_method="SSLCommerz",
#                 amount_paid=order.order_total,
#                 status="Completed",
#             )

            
#             order.status = "Completed"
#             order.payment = payment
#             order.save()

#             # CartItems will be automatically deleted
#             # Cart.objects.filter(user=request.user).delete()
#             session_key = request.COOKIES.get('key') 
            
#             cart = Cart.objects.filter(session=session_key)
#             cart.delete()
#             context = {
#                 "order": order,
#                 "transaction_id": tran_id,
#             }
#             return render(request, "orders/status.html", context)

            
#         else:
#             return HttpResponse({"status": "error", "message": "Payment failed"})

#     return render(request, "orders/status.html")
