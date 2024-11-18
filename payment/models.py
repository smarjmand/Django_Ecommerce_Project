from django.db import models
from django.contrib.auth.models import User
from store.models import Product

#------------------------------------------------------------------
# To save address in DB :
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=200, verbose_name='ایمیل')
    state = models.CharField(max_length=50, verbose_name='استان')
    city = models.CharField(max_length=50, verbose_name='شهر')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    zip_code = models.CharField(max_length=100, verbose_name='کدپستی')

    def __str__(self):
        return f'آدرس شماره {self.id}'

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'


#------------------------------------------------------------------
# To save orders in DB :
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    shipping_address = models.TextField()
    payment_amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    track_number = models.CharField(max_length=10, unique=True, db_index=True)
    is_payed = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f'سفارش - {self.id}'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


#------------------------------------------------------------------
# To save items of an order in DB :
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField()

    def __str__(self):
        return f'آیتم شماره {self.id}'

    class Meta:
        verbose_name = 'آیتم'
        verbose_name_plural = 'آیتم ها'
