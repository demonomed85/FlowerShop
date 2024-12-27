from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)  # Название цветка
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена цветка
    stock = models.PositiveIntegerField()  # Количество на складе
    photo = models.ImageField(upload_to='', null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=100)  # Имя клиента
    last_name = models.CharField(max_length=100)  # Фамилия клиента
    email = models.EmailField(unique=True)  # Email клиента
    phone_number = models.CharField(max_length=15)  # Телефон клиента
    address = models.TextField()  # Адрес доставки

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Связь с клиентом
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    delivery_date = models.DateField()  # Дата доставки
    desired_time = models.TimeField()  # Желаемое время доставки
    actual_delivery_time = models.TimeField(null=True, blank=True)  # Фактическое время доставки

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Связь с заказом
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Связь с товаром
    quantity = models.PositiveIntegerField()  # Количество товара в заказе

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in Order #{self.order.id}"


class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Связь с заказом
    courier = models.ForeignKey('Courier', on_delete=models.SET_NULL, null=True)  # Связь с курьером
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('delivered', 'Delivered')])  # Статус доставки

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    def __str__(self):
        return f"Доставка заказа №{self.order.id} - Статус: {self.status}"


class Courier(models.Model):
    name = models.CharField(max_length=100)  # Имя курьера
    phone_number = models.CharField(max_length=15)  # Телефон курьера
    city = models.CharField(max_length=100)  # Город

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return self.name

