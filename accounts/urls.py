
from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('edit_info/', views.edit_info, name='edit'),
    path('sign-up/', views.register, name='signup'), 
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify-email'),   
       
]
