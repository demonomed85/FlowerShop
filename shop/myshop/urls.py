from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('basket/', views.basket, name='basket'),
    path('item/', views.item, name='item'),
    path('logout/', views.logout, name='logout'),
    path('order/', views.order, name='order'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
]
