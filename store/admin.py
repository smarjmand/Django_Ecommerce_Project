from django.contrib import admin
from .models import Product, Category


#------------------------------------------------------------------
# To manage products in Django-Admin :
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'price','category', 'is_active', 'is_deleted']
    list_editable = ['is_active', 'is_deleted']


#------------------------------------------------------------------
# To manage categories in Django-Admin :
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'slug', 'is_active', 'is_deleted']
    list_editable = ['is_active', 'is_deleted']


#------------------------------------------------------------------
# Register models in Django-Admin :
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
