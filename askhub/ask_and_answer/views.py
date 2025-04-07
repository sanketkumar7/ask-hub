from django.shortcuts import render,HttpResponse

# Create your views here.
def dashbord(req):
    return HttpResponse('Welcome to Askhub')
