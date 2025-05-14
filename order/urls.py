
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('confirmed/', views.confirm_order, name='confirmed'),
    path("payments/", views.payment, name="payment"),
    path("payments/payment_status/", views.payment_status, name="payment_status"),
    path(
        "payments/sslc/complete/<val_id>/<tran_id>/", views.sslc_complete, name="sslc_complete",)
]

