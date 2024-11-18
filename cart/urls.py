from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_cart, name='shopping_cart_page'),
    path('add', views.cart_add, name='cart_add_view'),
    path('delete', views.cart_delete, name='card_delete_view'),
    path('update', views.cart_update, name='cart_update_view')
]
