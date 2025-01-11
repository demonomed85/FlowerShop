from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('basket/', views.basket, name='basket'),
    path('item/', views.item, name='item'),
    path('logout/', views.logout, name='logout'),
    path('order/', views.order, name='order'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('add_new_item/', views.add_new_item, name='add_new_item'),
    path('admin_only/', views.admin_only, name='admin_only'),
    path('courier/', views.courier, name='courier'),
    path('new_courier/', views.new_courier, name='new_courier'),
    path('delete_couriers/', views.delete_couriers, name='delete_couriers'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('edit_item/<int:item_id>/', edit_item, name='edit_item'),
    path('goods/', views.goods, name='goods'),
    path('delivery/', views.delivery, name='delivery'),
    path('orders/', views.orders, name='orders'),
    path('update_orders_status/', views.update_orders_status, name='update_orders_status'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('repeat_order/', views.repeat_order, name='repeat_order'),
]
