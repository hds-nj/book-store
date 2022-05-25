from re import T
from statistics import mode
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from account.models import Profile
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    class Meta :
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
    
    # parent = models.ForeignKey( 'self' , default=None , blank = True , null= True , on_delete=models.SET_NULL , related_name='children' , verbose_name='زیر دسته')
    title = models.CharField(max_length=200, verbose_name= "عنوان دسته بندی")
    name = models.CharField(max_length =100 , verbose_name="نام دستبندی")
    meta_description = models.TextField(max_length=200 , verbose_name="متاتگ")
    slug = models.SlugField(max_length=100, unique=True , verbose_name= "پیوند یکتا")
    status = models.BooleanField(default= True, verbose_name = "منتشر شود؟")
    position = models.IntegerField(verbose_name="پوزیشن")

    ordering = ["position"]
    
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("account:ProductList")


class Product(models.Model):
    """
    Model of Product Items for Save Detail Information for Show in Home Page
    """
    class Meta:
        verbose_name ='کتاب'
        verbose_name_plural = 'کتاب ها'
    title = models.CharField(max_length=50 , verbose_name='عنوان کتاب')
    metadescription = models.TextField(max_length=200 , verbose_name='متاتگ')
    slug = models.SlugField(max_length=100 , verbose_name='پیوند یکتا' ,unique=True)
    name = models.CharField(max_length=30 , verbose_name='نام کتاب ' , unique=True)
    image = models.ImageField(upload_to="media/products", verbose_name="تصویر", default="Unknown.jpg", blank=True)
    Category = models.ManyToManyField(Category, related_name="books", verbose_name="دستبندی" , null=True , blank=True)
    price = models.PositiveBigIntegerField(verbose_name="قیمت",)
    status = models.BooleanField(default= True, verbose_name = "منتشر شود؟")
    inventory = models.PositiveBigIntegerField(verbose_name="تعداد موجودی",)
    auther_name = models.CharField(max_length=24, null=True, default=None ,verbose_name="نویسنده") 
    featured = models.BooleanField(default=False, db_index=True, verbose_name="Recommended")
    description = models.TextField( max_length= 500 , verbose_name='توضیحات کتاب')
    def __str__(self):
        return self.name

    def category_published(self):
            return self.Category.filter(status= True)

    def get_absolute_url(self):
        return reverse("home")
        
    def category_to_str(self):
        return ", ".join([Category.name for Category in self.category_published()])
    category_to_str.short_description = "دسته بندی" 

    def category_to_sl(self):
            return ", ".join([Category.slug for Category in self.category_published()])
    category_to_sl.short_description = "دسته بندی"
       


class Order(models.Model):
    customer = models.ForeignKey(User , on_delete=models.SET_NULL , blank=True , null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False , null=True , blank=False)
    transaction_id = models.CharField(max_length=200 , null=True)
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.SET_NULL , blank=True , null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL ,null=True , blank=True )
    quantity = models.IntegerField(default=0 , null=True , blank=True)
    date_added = models.DateTimeField(auto_now_add=True)





