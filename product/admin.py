
   
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .admin import *
from .models import *

# Register your models here.

# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('position', 'title', 'slug', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')

admin.site.register(Category, CategoryAdmin)



class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title','name', 'slug', 'price', 'status', 'metadescription','description' )
    list_filter = ('status', 'price')
    search_fields = ('name', 'ShortSpecifications')
    # ordering = ['-status', '-publish']
    def category_to_str(self , obj):
            return ",".join([Category.title for Category in obj.category.all()])
    category_to_str.short_description = "دسته بندی"
admin.site.register(Product, ProductsAdmin)
