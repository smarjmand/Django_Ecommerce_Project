from django.urls import path
from . import views

urlpatterns = [

    # Payment for order :
    path('', views.checkout, name='checkout_page'),
    path('payment-request', views.payment_request, name='complete_order_view'),
    path('payment-result/<order>', views.verify_payment, name='payment_success_view'),

    # Order Tracking for users with no account :
    path('track-order', views.track_order, name='track_order_page'),
    path('track-order/detail/<order>', views.order_detail, name='track_order_detail_page'),
]