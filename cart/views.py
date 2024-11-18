from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse


#------------------------------------------------------------------
# To show/update/delete shopping cart items :
def shopping_cart(request):
    cart = Cart(request=request)
    context = {'cart': cart}
    return render(request, 'cart_items.html', context)


#------------------------------------------------------------------
# To add/update an item in shopping cart :
def cart_add(request):
    cart = Cart(request=request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)
        cart_quantity = cart.__len__()

        return JsonResponse({'qty': cart_quantity})


#------------------------------------------------------------------
# To delete an item from shopping cart :
def cart_delete(request):
    cart = Cart(request=request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id)
        cart_quantity = cart.__len__()
        cart_total_price = cart.get_total_cart_price()
        return JsonResponse({
            'qty': cart_quantity,
            'cart_total_price': cart_total_price
        })


#------------------------------------------------------------------
# To update/quantity of an item in shopping cart :
def cart_update(request):
    cart = Cart(request=request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        if product_quantity < 1:
            product_quantity = 1
        cart.update(product_id, product_quantity)
        cart_quantity = cart.__len__()
        cart_total_price = cart.get_total_cart_price()
        return JsonResponse({
            'qty': cart_quantity,
            'cart_total_price': cart_total_price
        })
