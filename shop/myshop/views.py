from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CartItem, Cart, Item, Order, OrderStatus, OrderItem, User, Courier, Delivery, TelegramUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import RegistrationForm
import json
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import TelegramUserSerializer
from static.TG.config import TOKEN
import requests

caption = "FlowerShop"


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

def index(request):
    items = Item.objects.all()
    data = {
        'caption': caption,
        'items': items
    }
    return render(request, 'myshop/index.html', data)


@login_required(login_url='/login')
def basket(request):
    # Проверяем наличие customer у пользователя
    if hasattr(request.user, 'customer'):
        cart = Cart.objects.filter(customer=request.user.customer).first()
        items = cart.items.all() if cart else []
    else:
        items = []  # Если нет customer, корзина будет пустой

    # Вычисляем итоговую стоимость
    total_cost = sum(item.item.price * item.quantity for item in items)

    data = {
        'caption': 'Корзина',
        'cart_items': items,
        'total_cost': total_cost,  # Добавляем итоговую стоимость в контекст
    }

    return render(request, 'myshop/basket.html', data)


@login_required(login_url='/login')
def remove_from_cart(request, item_id):
    if hasattr(request.user, 'customer'):
        cart = Cart.objects.filter(customer=request.user.customer).first()
        if cart:
            cart.items.filter(id=item_id).delete()  # Удаляем товар из корзины
    return redirect('basket')





@login_required(login_url='/login')  # Указываем URL для страницы авторизации
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Пожалуйста, авторизуйтесь для добавления товара в корзину.'})

@csrf_exempt
@login_required(login_url='/login')
def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')

        cart = Cart.objects.get(customer=request.user.customer)
        print(f'Cart - {cart.id}')
        cart_item = CartItem.objects.get(cart=cart, id=item_id)
        print(f'Cart - {cart.id}')
        print(f'cart_item - {cart_item.id}')
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        # Пересчитываем общую стоимость
        total_cost = sum(item.item.price * item.quantity for item in cart.items.all())

        return JsonResponse({'success': True, 'total_cost': total_cost})
    return JsonResponse({'success': False}, status=400)


def item(request):
    data = {
        'caption': caption
    }
    return render(request, 'myshop/item.html', data)


def logout(request):
    auth_logout(request)  # Завершение сессии пользователя
    return redirect('index')


@login_required(login_url='/login')
def order(request):
    customer = request.user.customer
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []

    order_number = "ORD-{}".format(timezone.now().strftime("%Y%m%d%H%M%S"))
    current_date = timezone.now().date()
    delivery_date = current_date + timezone.timedelta(days=1)

    orders = Order.objects.filter(customer=customer)
    hours = list(range(8, 20))

    data = {
        'caption': caption,
        'order_number': order_number,
        'current_date': current_date.strftime("%d.%m.%Y"),
        'recipient_name': f"{customer.first_name} {customer.last_name}",
        'delivery_date': delivery_date.strftime("%d.%m.%Y"),
        'address': customer.address,
        'items': items,
        'orders': orders,  # Передаем заказы в контекст
        'hours': hours
    }
    return render(request, 'myshop/order.html', data)


@login_required(login_url='/login')
def repeat_order(request):
    if request.method == "POST":
        customer = request.user.customer
        order_id = request.POST.get('order_id')

        # Получаем предыдущий заказ по ID
        previous_order = get_object_or_404(Order, id=order_id, customer=customer)

        cart, created = Cart.objects.get_or_create(customer=customer)

        total_cost = 0
        for item in previous_order.items.all():
            # Получаем товар через связь с OrderItem
            product = item.item
            total_cost += product.price * item.quantity  # Считаем общую стоимость

            # Добавляем товар в корзину
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product, quantity=item.quantity)
            if not created:
                cart_item.quantity += item.quantity  # Увеличиваем количество, если товар уже в корзине
            cart_item.save()

        data = {
            'caption': 'Корзина',
            'cart_items': previous_order.items.all(),  # Передаем все товары из предыдущего заказа
            'total_cost': total_cost,
        }

        return render(request, 'myshop/basket.html', data)

    return redirect('order')  # Если не POST, перенаправляем обратно на страницу заказов

@login_required(login_url='/login')
def create_order(request):
    if request.method == "POST":

        customer = request.user.customer
        order_number = request.POST.get('order_number')
        delivery_date = request.POST.get('delivery_date')
        desired_time = request.POST.get('desired_time')
        address = request.POST.get('address')


        order = Order.objects.create(customer=customer, order_number=order_number, delivery_date=delivery_date, desired_time=desired_time, address=address, status=OrderStatus.objects.get(name='Новый'))

        cart = Cart.objects.filter(customer=customer).first()
        if cart:
            for cart_item in cart.items.all():
                OrderItem.objects.create(order=order, item=cart_item.item, quantity=cart_item.quantity)
            cart.items.all().delete()  # Очистка корзины после создания заказа

        return redirect('order')  # Перенаправляем на страницу заказов



def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']

            # Проверка существования пользователя
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует.')
                print ('Пользователь с таким именем уже существует.')
                return render(request, 'myshop/registration.html', {'form': form})

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует.')
                print ('Пользователь с таким email уже существует.')
                return render(request, 'myshop/registration.html', {'form': form})

            # Создание пользователя
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Проверка существования Customer
            #if Customer.objects.filter(user=user).exists():
            #    messages.error(request, 'Клиент с этим пользователем уже зарегистрирован.')
            #    print(f'Клиент с этим пользователем уже зарегистрирован. {user}')
            #    return render(request, 'myshop/registration.html', {'form': form})

            # Создание объекта Customer
            #customer = Customer(
            #    user=user,
            #    first_name=first_name,
            #    last_name=last_name,
            #    email=email,
            #    phone_number=phone_number,
            #    address=address
            #)
            #print(customer)
            #customer.save()

            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти в систему.')
            return redirect('login')
    else:
        form = RegistrationForm()

    # Возвращаем форму в любом случае
    data = {
        'form': form
    }

    return render(request, 'myshop/registration.html', data)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            #messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

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


@login_required
def admin_only(request):
    # Проверяем, принадлежит ли пользователь к группе "Владелец" или "Менеджер"
    user_groups = request.user.groups.values_list('name', flat=True)

    if "Владелец" in user_groups or "Менеджер" in user_groups:
        items = Item.objects.all()
        data = {
            'caption': caption,
            'items': items
        }
        return render(request, 'myshop/admin_only.html', data)
    else:
        # Если пользователь авторизован, но не в нужной группе
        return render(request, 'myshop/access_denied.html')


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
    orders = Order.objects.prefetch_related('items__item', 'customer', 'delivery__courier', 'status').all()
    couriers = Courier.objects.all()

    data = {
        'orders': orders,
        'caption': caption,
        'couriers' : couriers,
    }
    return render(request, 'myshop/orders_admin.html', data)


def update_orders_status(request):
    if request.method == 'POST':
        selected_orders = request.POST.getlist('selected_orders')
        action = request.POST.get('action')

        if not selected_orders:
            messages.error(request, "Выберите хотя бы один заказ.")
            return redirect('orders')

        for order_id in selected_orders:
            try:
                order = Order.objects.get(id=order_id)
                current_status = order.status
                new_status = None

                if action == 'next':
                    new_status = get_next_status(current_status)
                elif action == 'previous':
                    new_status = get_previous_status(current_status)

                if new_status:
                    order.status = new_status
                    order.save()
                    messages.success(request, f"Статус заказа ID {order.id} успешно изменен на {new_status.name}.")
                else:
                    messages.warning(request, f"Перевод статуса заказа ID {order.id} невозможен.")

            except Order.DoesNotExist:
                messages.error(request, f"Заказ с ID {order_id} не найден.")
            order.set_status(order.status)

        return redirect('orders')

def get_next_status(current_status):
    statuses = OrderStatus.objects.all().order_by('id')
    status_list = list(statuses)

    try:
        current_index = status_list.index(current_status)
        if current_index < len(status_list) - 1:
            return status_list[current_index + 1]
    except ValueError:
        return None

def get_previous_status(current_status):
    statuses = OrderStatus.objects.all().order_by('id')
    status_list = list(statuses)

    try:
        current_index = status_list.index(current_status)
        if current_index > 0:
            return status_list[current_index - 1]
    except ValueError:
        return None
@require_POST
def delete_couriers(request):
    # Получаем список ID курьеров из формы
    courier_ids = request.POST.getlist('courier_ids')

    if courier_ids:
        Courier.objects.filter(id__in=courier_ids).delete()

    return redirect('courier')


@require_POST
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
    except Item.DoesNotExist:
        pass
    return redirect('goods')

def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'myshop/add_new_item.html', {'item': item})


# Функция для отправки сообщения в Telegram
def send_message(user_id, text):
    bot_token = 'TOKEN'  # Замените на ваш токен бота
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    payload = {
        'chat_id': user_id,
        'text': text,
    }

    response = requests.post(url, json=payload)
    return response.json()