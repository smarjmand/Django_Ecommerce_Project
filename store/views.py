from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator


#------------------------------------------------------------------
# To show all products :
def index_page(request):
    products = Product.objects.filter(is_active=True, is_deleted=False)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {'page_obj': page_object}
    return render(request, 'store/index.html', context)


#------------------------------------------------------------------
# To get categories for navigation bar :
def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


#------------------------------------------------------------------
# To show product detail and add it to shopping cart :
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)


#------------------------------------------------------------------
# To filter products based on category :
def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True, is_deleted=False)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'category': category}
    return render(request, 'store/products_by_category.html', context)
