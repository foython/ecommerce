from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
import random
import string
from datetime import datetime, timedelta
from order.models import OrderItem, Order
from .forms import UserCreationForm

# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('home')
        else:
            messages.info(request, 'Username Password not matched')
            return redirect(request.path)
    else:
        return render(request, 'login.html')
    


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def user_profile(request):    
    orders = Order.objects.filter(user__id=request.user.id).order_by('-id') 
    order_items = OrderItem.objects.filter(order__user__id=request.user.id).order_by('order__id')    
    context = { 'orders':orders, 'items':order_items}
    cooki = request.COOKIES.get('key')    
    if not cooki:
        cookie_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        response = render(request, 'profile.html', context)
        response.set_cookie('key', cookie_value, expires=datetime.utcnow()+timedelta(days=15))
        return response
    return render(request, 'profile.html', context)


def register(request):
    sform = UserCreationForm()
    if request.method == 'POST':
        rform = UserCreationForm(request.POST)
        if rform.is_valid():
            rform.save()
            return redirect('login')
    return render(request, 'registration.html', {'form': sform})

    
