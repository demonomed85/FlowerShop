from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'myshop/index.html')

def basket(request):
    return render(request, 'myshop/basket.html')

def item(request):
    return render(request, 'myshop/item.html')

def logout(request):
    return render(request, 'myshop/logout.html')

def order(request):
    return render(request, 'myshop/order.html')

def registration(request):
    return render(request, 'myshop/registration.html')

def login(request):
    return render(request, 'myshop/login.html')

