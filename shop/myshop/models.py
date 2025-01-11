from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='', null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь с моделью User
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    desired_time = models.TimeField()
    actual_delivery_time = models.TimeField(null=True, blank=True)
    address = models.TextField()
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    @property
    def total_cost(self):
        return sum(
            item.item.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

    def set_status(self, status):
        #self.status = status
        #self.save()
        if status.name == 'В доставке':
            Delivery.objects.create(order=self)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in Order #{self.order.id}"


class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    courier = models.ForeignKey('Courier', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('delivered', 'Delivered')])

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    def __str__(self):
        return f"Доставка заказа №{self.order.id} - Статус: {self.status}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def str(self):
        return f"{self.quantity} of {self.item.name} in Cart"

@receiver(post_save, sender=Delivery)
def update_order_status_on_delivery(sender, instance, **kwargs):
    if instance.status == 'delivered':
        instance.order.set_status(OrderStatus.objects.get(status='completed'))


class Courier(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return self.name

