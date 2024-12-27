from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import *


caption = "FlowerShop"


def index(request):
    items = Item.objects.all()
    data = {
        'caption': caption,
        'items': items
    }
    return render(request, 'myshop/index.html', data)


def basket(request):
    data = {
        'caption': caption
    }
    return render(request, 'myshop/basket.html', data)


def item(request):
    data = {
        'caption': caption
    }
    return render(request, 'myshop/item.html', data)


def logout(request):
    data = {
        'caption': caption
    }
    return render(request, 'myshop/logout.html', data)


def order(request):
    data = {
        'caption': caption
    }
    return render(request, 'myshop/order.html', data)


def registration(request):
    data = {
        'caption': caption
    }
    return render(request, 'myshop/registration.html', data)


def login(request):
    data = {
        'caption': caption
    }
    return render(request, 'myshop/login.html', data)


def add_new_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        photo = request.FILES.get('photo')

        item = Item(name=name, price=price, stock=stock, photo=photo)
        item.save()

        return redirect('admin_only')

    data = {
        'caption': caption
    }
    return render(request, 'myshop/add_new_item.html', data)


def admin_only(request):
    items = Item.objects.all()

    data = {
        'caption': caption,
        'items': items
    }
    return render(request, 'myshop/admin_only.html', data)


def courier(request):
    couriers = Courier.objects.all()
    data = {
        'caption': caption,
        'couriers': couriers
    }
    return render(request, 'myshop/courier_admin.html', data)


def delivery(request):
    delivery = Delivery.objects.all()
    data = {
        'caption': caption,
        'delivery': delivery
    }
    return render(request, 'myshop/delivery_admin.html', data)

def new_courier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')

        courier = Courier(name=name, phone_number=phone_number, city=city)
        courier.save()

        return redirect('courier')
    data = {
        'caption': caption
    }
    return render(request, 'myshop/new_courier.html', data)


def goods(request):
    items = Item.objects.all()
    data = {
        'items': items,
        'caption': caption
    }
    return render(request, 'myshop/goods_admin.html', data)



def orders(request):
    orders = Order.objects.all()
    data = {
        'orders': orders,
        'caption': caption
    }
    return render(request, 'myshop/orders_admin.html', data)



@require_POST
def delete_couriers(request):
    # Получаем список ID курьеров из формы
    courier_ids = request.POST.getlist('courier_ids')

    # Удаляем курьеров с указанными ID
    if courier_ids:
        Courier.objects.filter(id__in=courier_ids).delete()

    # Перенаправляем обратно на страницу учета курьеров
    return redirect('courier')


@require_POST
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
    except Item.DoesNotExist:
        pass  # Обработайте ошибку, если необходимо
    return redirect('goods')

def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    # Логика для обработки формы редактирования
    # Предполагается, что у вас есть соответствующий шаблон и форма
    return render(request, 'myshop/add_new_item.html', {'item': item})