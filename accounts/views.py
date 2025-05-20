from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from accounts.forms import CustomUserRegistrationForm, CustomUserChangeForm
from accounts.models import CustomUser
from order.models import Order, OrderItem
from accounts.utils import send_password_reset_email, send_verification_email
from datetime import timedelta
import random
from datetime import datetime
import string


def register(request):
    form = CustomUserRegistrationForm()
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(request, user)
            messages.info(request, "We have sent you an verfication email")
            return redirect("login")
        # TODO: show form errors in template
    return render(request, "register.html", {'form': form})


def user_login(request): 
    if request.user.is_authenticated:
        return redirect("profile")
       
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")               

        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, "Invalid username or password.")
        elif not user.is_verified:
            messages.error(request, "Your email is not verified yet.")
        else:
            login(request, user)            
            return redirect("profile")

    return render(request, "login.html")



@login_required
def user_logout(request):
    logout(request)
    list(messages.get_messages(request))
    return redirect('login')


@login_required
def user_profile(request): 
    user = CustomUser.objects.get(id=request.user.id)   
    orders = Order.objects.filter(user__id=request.user.id).order_by('-id') 
    order_items = OrderItem.objects.filter(order__user__id=request.user.id).order_by('order__id')    
    context = { 'orders':orders, 'items':order_items, 'user': user}
    cooki = request.COOKIES.get('key')    
    if not cooki:
        cookie_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        response = render(request, 'profile.html', context)
        response.set_cookie('key', cookie_value, expires=datetime.utcnow()+timedelta(days=15))
        return response
    return render(request, 'profile.html', context)


@login_required
def edit_info(request):  
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  
            return redirect('profile')
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_info.html', {'form': form})
      


# @login_required
# def user_profile(request):
#     user = request.user

#     if request.method == "POST":
#         # TODO: use a form and show form errors in template
#         # TODO: let user change password
#         user.email = request.POST.get("email", user.email)
#         user.mobile = request.POST.get("mobile", user.mobile)
#         user.address_line_1 = request.POST.get("address_line_1", user.address_line_1)
#         user.address_line_2 = request.POST.get("address_line_2", user.address_line_2)
#         user.city = request.POST.get("city", user.city)
#         user.postcode = request.POST.get("postcode", user.postcode)
#         user.country = request.POST.get("country", user.country)
#         user.save()

#         return redirect("profile")

#     context = {"user_info": user}
#     return render(request, "profile.html", context)


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, "Your email has been verified successfully.")
        return redirect("login")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("signup")


















# from django.shortcuts import render, redirect, HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.urls import reverse
# import random
# import string
# from datetime import datetime, timedelta
# from order.models import OrderItem, Order
# from .forms import UserCreationForm

# # Create your views here.

# def user_login(request):
#     if request.user.is_authenticated:
#         return redirect('home')
    
#     elif request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if 'next' in request.POST:
#                 return redirect(request.POST['next'])
#             else:
#                 return redirect('home')
#         else:
#             messages.info(request, 'Username Password not matched')
#             return redirect(request.path)
#     else:
#         return render(request, 'login.html')
    


# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('login'))





# def register(request):
#     sform = UserCreationForm()
#     if request.method == 'POST':
#         rform = UserCreationForm(request.POST)
#         if rform.is_valid():
#             rform.save()
#             return redirect('login')
#     return render(request, 'registration.html', {'form': sform})

    
