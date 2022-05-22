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
    image = models.FileField(upload_to="media/products", verbose_name="تصویر",default="Unknown.jpg", blank=True)
    Category = models.ManyToManyField(Category, related_name="books", verbose_name="دستبندی" , null=True , blank=True)
    price = models.PositiveBigIntegerField(verbose_name="قیمت",)
    status = models.BooleanField(default= True, verbose_name = "منتشر شود؟")
    inventory = models.PositiveBigIntegerField(verbose_name="تعداد موجودی",)
    properties = models.CharField(max_length=24, null=True, default=None) 
    featured = models.BooleanField(default=False, db_index=True, verbose_name="Recommended")
    description = models.TextField( max_length= 500 , verbose_name='توضیحات کتاب')

    def category_published(self):
            return self.Category.filter(status= True)
    
    def category_to_str(self):
        return ", ".join([Category.name for Category in self.category_published()])
    category_to_str.short_description = "دسته بندی" 

    @property
    def final_price(self) -> int:
      
        result = self.price
        if result == self.price: 
                self.price = None
                self.save()
        return result
    final_price.fget.short_description = ("قیمت نهایی")  # like verbose name for panel admin

    def change_inventory(self, new_value: int):
        """
        Method for Apply Change Number of Inventory After Paid or Cancelng Order
        """
        
        if self.inventory - new_value >= 0:
            self.inventory -= new_value
            self.save()
        else: raise ValueError("شماره موجودی نمی تواند عدد منفی باشد!r!")

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)        

class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE , null=True , blank=True)
    total = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True, verbose_name="Is active")

    def __str__(self):
        return "Cart - " + self.profile.user.username


class CartItem(models.Model):
    good = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    material = models.CharField(max_length=10, default='rubber', verbose_name="Material")

    def __str__(self):
        return self.cart.profile.user.username + " - " + self.good.name


@receiver(pre_save, sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    if not instance._state.adding:
        db_instace = CartItem.objects.filter(cart=instance.cart, good=instance.good)[0]
        if db_instace.good.price_acc is None or db_instace.good.price >= db_instace.good.price:
            prev_cost = db_instace.quantity * db_instace.good.price
        else:
            prev_cost = db_instace.quantity * db_instace.good.price_acc
    else:
        prev_cost = 0.0

    if instance.good.price_acc is None or instance.good.price >= instance.good.price:
        cost = instance.quantity * instance.good.price
    else:
        cost = instance.quantity * instance.good.price_acc
    instance.cart.total -= prev_cost
    instance.cart.total += cost
    instance.cart.save()
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#     order_date = models.DateField(null=True)
#     payment_type = models.CharField(max_length=100, null=True)
#     payment_id = models.CharField(max_length=100, null=True)

#     def add_to_cart(self, book_id):
#         book = Product.objects.get(pk=book_id)
#         try:
#             preexisting_order = Order.objects.get(book=book, cart=self)
#             preexisting_order.quantity += 1
#             preexisting_order.save()
#         except Order.DoesNotExist:
#             new_order = Order.objects.create(
#                 book=book, 
#                 cart=self,
#                 quantity = 1
#             )
#             new_order.save

#     def remove_from_cart(self, book_id):
#         book = Product.objects.get(pk=book_id)
#         try:
#             preexisting_order = Order.objects.get(book=book, cart=self)
#             if preexisting_order.quantity > 1:
#                 preexisting_order.quantity -= 1
#                 preexisting_order.save()
#             else: 
#                 preexisting_order.delete()
#         except Order.DoesNotExist:
#             pass


# class Order(models.Model):
#     book = models.ForeignKey(Product, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     quantity = models.IntegerField()        