
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add/cart', views.addtocart, name='add_to_cart'),
    path('removecart/<int:id>', views.remove_cart, name='remove_cart'),

]
