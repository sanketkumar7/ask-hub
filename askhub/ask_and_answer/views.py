from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import make_password
from .models import User

from .forms import user_form
# Create your views here.
def home_page(req):
    return render(req,'aaa/home.html')

def login_user(req):
    if req.method=="POST":
        username=req.POST['username']
        password=req.POST['password']
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            user=None
        if user and user.check_password(password):
            login(req,user)
            messages.success(req,f'Welcome {user.username}.')
            return redirect('home')
        else:
            messages.error(req,'Invalid Username or Password.')
    return render(req,'aaa/login.html')
def register_user(req):
    form= user_form()
    if req.method=="POST":
        form=user_form(req.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.password=make_password(user.password)
            user.save()
            messages.success(req,f'{user.username} Registered. Please Log in.')
            return redirect('login_user')
    context={
        'form':form
    }
    return render(req,'aaa/registration.html',context)

def logout_user(req):
    logout(req)
    messages.success(req,'Successfully logout. Please log in.')
    return redirect('login_user')