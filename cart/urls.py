
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add/cart', views.addtocart, name='add_to_cart'),
    path('remove/cart/<int:id>', views.remove_cart, name='remove_cart'),
    path('remove/cart/', views.remove_cart, name='remove_full_cart'),
    path('update/cart/', views.update_cart, name='update_cart'),
]
