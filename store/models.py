from django.db import models


#------------------------------------------------------------------
# To save categories in DB :
class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='عنوان')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, verbose_name='اسلاگ')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


#------------------------------------------------------------------
# To save products in DB :
class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    brand = models.CharField(max_length=50, default='متفرقه', verbose_name='برند')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name='دسته بندی')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    slug = models.SlugField(max_length=250,unique=True, allow_unicode=True, verbose_name='اسلاگ')
    price = models.IntegerField(default=0, verbose_name='قیمت')
    image = models.ImageField(upload_to='images/products/',blank=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='موجود')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return f'{self.title}/{self.brand}'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
