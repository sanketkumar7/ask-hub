from django.urls import path
from .views import *
urlpatterns = [
    path('',home_page,name='home'),
    path('login-user',login_user,name='login_user'),
    path('register-user',register_user,name='register_user'),
    path('logout-user',logout_user,name='logout_user'),
]
