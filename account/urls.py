from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Registration :
    path('register', views.register, name='register_page'),
    path('email-verification-sent', views.email_verification_sent, name='email_verification_sent'),
    path('email-verification/<uidb64>/<token>', views.email_verification, name='email_verification'),
    path('email-verification-success', views.email_verification_success, name='email_verification_success'),
    path('email-verification-failed', views.email_verification_failed, name='email_verification_failed'),
    # Account Management :
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_view, name='logout_view'),
    path('dashboard', views.dashboard, name='dashboard_page'),
    path('address', views.manage_address, name='manage_address_page'),
    path('orders', views.orders, name='orders_page'),
    path('odrer-detail/<order_pk>', views.order_detail, name='order_detail_page'),
    # Reset Password :
    path(
        'reset-password',
        views.CustomPasswordResetView.as_view(template_name='account/reset/password_reset.html'),
        name='reset_password'
    ),
    path(
        'reset-password/sent',
        auth_views.PasswordResetDoneView.as_view(template_name='account/reset/password_reset_sent.html'),
        name='password_reset_done'
    ),
    path(
        'reset-password/<uidb64>/<token>',
        views.CustomPasswordResetConfirmView.as_view(template_name='account/reset/password_reset_form.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset-password/complete',
        auth_views.PasswordResetCompleteView.as_view(template_name='account/reset/password_reset_complete.html'),
        name='password_reset_complete'
    )

]