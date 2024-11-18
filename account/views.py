from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.sites.shortcuts import get_current_site
from .utils import user_token_generator, send_verification_email
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from payment.forms import Address, AddressForm
from payment.models import Order


#------------------------------------------------------------------
# To register new user :
def register(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            # Save user in DB:
            user_object = form.save()
            user_object.is_active = False
            user_object.save()

            # Send verification email:
            site_domain = get_current_site(request)
            send_verification_email(user=user_object, domain=site_domain.domain)

            return redirect('email_verification_sent')

        context = {'form': form}

    return render(request, 'account/register.html', context)


#------------------------------------------------------------------
# To send verification email to new user :
def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)

    # Activate user's account :
    if user and user_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email_verification_success')

    return redirect('email_verification_failed')


#------------------------------------------------------------------
# To show messages for verifying account :
def email_verification_sent(request):
    return render(request, 'account/email/email_verification_sent.html')


def email_verification_success(request):
    return render(request, 'account/email/email_verification_success.html')


def email_verification_failed(request):
    return render(request, 'account/email/email_verification_failed.html')


#------------------------------------------------------------------
# To login user :
def login_page(request):
    form = LoginForm()
    context = {'form': form}

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'به سفارش چی خوش آمدید')
                return redirect('dashboard_page')

        context = {'form': form}

    return render(request, 'account/login.html', context)


#------------------------------------------------------------------
# To logout user :
def logout_view(request):
    logout(request)
    messages.success(request, 'از حساب کاربری خود خارچ شدید !')
    return redirect('store_index_page')


#------------------------------------------------------------------
# To update user's infos and delete account :
@login_required(login_url='login_page')
def dashboard(request):
    user_form = UpdateUserForm(instance=request.user)
    context = {'form': user_form}

    if request.method == 'POST':

        # To delete user's account :
        if request.POST.get('action') == 'delete':
            user = User.objects.get(id=request.user.id)
            user.delete()
            messages.success(request, 'حساب کاربری شما با موفقیت حذف گردید')
            return redirect('store_index_page')

        # To update user's infos :
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'اطلاعات حساب کاربری شما با موفقیت تغییر یافت')
            return redirect('dashboard_page')
        context = {'form': user_form}

    return render(request, 'account/dashboard.html', context)


#------------------------------------------------------------------
# To customize verification-email that being sent to user :
class CustomPasswordResetView(PasswordResetView):
    subject_template_name = 'account/reset/password_reset_subject.txt'
    email_template_name = 'account/reset/password_reset_email.html'


#------------------------------------------------------------------
# To customize new-password form :
class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields['new_password1'].label = 'کلمه عبور جدید*'
        self.fields['new_password2'].label = 'تکرار کلمه عبور جدید*'

        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


#------------------------------------------------------------------
# To save address for users with account :
@login_required(login_url='login_page')
def manage_address(request):
    try:
        user_address = Address.objects.get(user_id=request.user.id)
    except Address.DoesNotExist:
        user_address = None

    form = AddressForm(instance=user_address)
    context = {'form': form}

    if request.method == 'POST':
        form = AddressForm(data=request.POST, instance=user_address)

        # To delete current user's address :
        if request.POST.get('action') == 'delete':
            if user_address is not None:
                user_address.delete()
                messages.success(request, 'آدرس شما با موفقیت حذف گردید')
            else:
                messages.success(request, 'برای حذف آدرس ابتدا آدرسی ثبت کنید')
            return redirect('manage_address_page')

        # To update or save user's address
        if form.is_valid():
            address_object: Address = form.save(commit=False)
            address_object.user = request.user
            address_object.save()
            messages.success(request, 'آدرس شما ثبت گردید')
            return redirect('manage_address_page')

        context = {'form': form}

    return render(request, 'account/address.html', context)


#------------------------------------------------------------------
# To track user's order with account :

@login_required(login_url='login_page')
def orders(request):
    try:
        shops = Order.objects.filter(user_id=request.user.id)
        print(shops)
    except Order.DoesNotExist:
        shops = None

    context = {'orders': shops}
    return render(request, 'account/orders.html', context)


@login_required(login_url='login_page')
def order_detail(request, order_pk):
    order = get_object_or_404(Order, id=order_pk)
    context = {'order': order}
    return render(request, 'account/order_detail.html', context)
