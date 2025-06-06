from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('select_sub', views.send_sub, name='send_sub'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/<str:name>', views.ShopView.as_view(), name='filtershop'),    
    path('details/<int:id>', views.DetailsView.as_view(), name='details'), 
    path('review/<int:product_id>', views.submit_review, name='submit_review'),   
    
]

 #