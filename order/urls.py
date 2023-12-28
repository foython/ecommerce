
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('confirmed/', views.confirm_order, name='confirmed'),
    
]
