from django.shortcuts import render, redirect, get_object_or_404
from .forms import Address, AddressForm
from django.http import JsonResponse, HttpRequest
from cart.cart import Cart
from .models import Order, OrderItem
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.conf import settings
import json
import requests
from django.db.models import Q


#------------------------------------------------------------------
# To pay the order :
def checkout(request):
    cart = Cart(request)

    if cart.get_total_cart_price() == 0:
        messages.success(request, 'سبد خرید شما خالی است')
        return redirect('shopping_cart_page')

    if request.user.is_authenticated:
        try:
            user_address = Address.objects.get(user_id=request.user.id)
            context = {'form': AddressForm(instance=user_address)}
            return render(request, 'payment/checkout.html', context)
        except Address.DoesNotExist:
            context = {'form': AddressForm()}
            return render(request, 'payment/checkout.html', context)

    else:
        context = {'form': AddressForm()}
        return render(request, 'payment/checkout.html', context)


#------------------------------------------------------------------
# To track order for users with no account :
def track_order(request):

    if request.method == 'POST':
        track_number = request.POST.get('track_number') or None
        email = request.POST.get('email') or None

        if track_number is None and email is None:
            messages.success(request, 'برای جستجو وارد کردن شماره پیگیری یا ایمیل الزامی است')

        else:
            order = Order.objects.filter(Q(track_number=track_number) | Q(email=email))

            if len(order) != 0:
                print(order, type(order), print(len(order)))
                context = {'orders': order}
                return render(request, 'payment/orders.html', context)
            else:
                messages.success(request, 'سفارشی با این مشخصات پیدا نشد !')

    return render(request, 'payment/track_order.html')


def order_detail(request, order):
    order = get_object_or_404(Order, id=order)
    context = {'order': order}
    return render(request, 'payment/order_detail.html', context)


#------------------------------------------------------------------
# To pay through ZarrinPal :
def payment_request(request: HttpRequest):
    full_name = request.POST.get('full_name')
    email = request.POST.get('email')

    order_address = ''
    for item in list(request.POST.values())[1:6]:
        order_address += f'{item}\n'

    cart = Cart(request)
    total_cost = cart.get_total_cart_price()

    if total_cost == 0:
        messages.success(request, 'سبد خرید شما خالی است')
        return redirect('shopping_cart_page')

    # for authenticated users :
    if request.user.is_authenticated:
        order_object = Order.objects.create(
            user=request.user, full_name=full_name,
            email=email, track_number=get_random_string(10),
            shipping_address=order_address, payment_amount=total_cost
        )
        for item in cart:
            OrderItem.objects.create(
                user=request.user, order_id=order_object.id,
                product=item['product'], quantity=item['qty'],
                price=item['price'],
            )
    # for guest users :
    else:
        order_object = Order.objects.create(
            full_name=full_name, email=email,
            shipping_address=order_address,
            payment_amount=total_cost,
            track_number=get_random_string(10)
        )
        for item in cart:
            OrderItem.objects.create(
                order_id=order_object.id,
                product=item['product'],
                quantity=item['qty'],
                price=item['price']
            )
    req_data = {
        "merchant_id": settings.MERCHANT,
        "amount": total_cost * 10,
        "callback_url": 'http://127.0.0.1:8080/pay/payment-result/'+ str(order_object.id),
        "description": 'خرید از سفارش چی'
    }

    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=settings.ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(settings.ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        context = {
            'msg': e_message,
            'order': order_object,
            'order_items': order_object.orderitem_set.all()
        }
        return render(request, 'payment/payment_failed.html', context)


#------------------------------------------------------------------
# To receive payment result from ZarrinPal :
def verify_payment(request: HttpRequest, order):
    t_authority = request.GET['Authority']

    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}

        try:
            order_object = Order.objects.get(id=order)
        except Order.DoesNotExist:
            raise 404

        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order_object.payment_amount * 10,
            "authority": t_authority
        }
        req = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order_object.is_payed = True
                order_object.payment_id = req.json()['data']['ref_id']
                order_object.save()

                for key in list(request.session.keys()):
                    if key == 'session_key':
                        del request.session[key]

                context = {
                    'payed': True,
                    'msg': None,
                    'order': order_object
                }
                return render(request, 'payment/payment_result.html', context)
            elif t_status == 101:
                context = {
                    'payed': False,
                    'msg': 'این تراکنش قبلا ثبت شده است',
                    'order': order_object
                }
                return render(request, 'payment/payment_result.html', context)
            else:
                context = {
                    'payed': False,
                    'msg': str(req.json()['data']['message']),
                    'order': order_object
                }
                return render(request, 'payment/payment_result.html', context)
        else:
            e_message = req.json()['errors']['message']
            context = {
                'payed': False,
                'msg': e_message,
                'order': order_object
            }
            return render(request, 'payment/payment_result.html', context)
    else:
        context = {
            'payed': False,
            'msg': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد',
            'order': None
        }
        return render(request, 'payment/payment_result.html', context)