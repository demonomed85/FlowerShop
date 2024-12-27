from django.contrib import admin

from .models import Item
admin.site.register(Item)

from .models import Customer
admin.site.register(Customer)

from .models import Order
admin.site.register(Order)

from .models import OrderItem
admin.site.register(OrderItem)

from .models import Delivery
admin.site.register(Delivery)

from .models import Courier
admin.site.register(Courier)

# Register your models here.

