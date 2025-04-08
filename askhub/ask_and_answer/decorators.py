from django.contrib import messages
from django.shortcuts import redirect
def unauthenticated(func):
    def wrapper_func(req,*args, **kwargs):
        if req.user.is_authenticated:
            messages.success(req,f'Welcome back {req.user.username}!')
            return redirect('home')
        return func(req,*args, **kwargs)
    return wrapper_func