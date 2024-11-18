from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='store_index_page'),
    path('product/<slug>', views.product_detail, name='product_detail_page'),
    path('categories/<slug>', views.products_by_category, name='products_by_category_page'),


]