

# class Order(models.Model):
#     class Meta:
#         verbose_name="سفارش "
#         verbose_name_plural =  "سفارشات"
#     STATUSES = {
#         'P': ("Paid"),
#         'U': ("Unpaid"),
#         'C': ("Canceled")
#     }
#     status = models.CharField(max_length=1, default='U', verbose_name="وضعیت سفارش", 
#         choices=[(key, value) for key, value in STATUSES.items()])
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     shippingPrice = models.DecimalField(
#         max_digits=7, decimal_places=2, null=True, blank=True)
#     totalPrice = models.DecimalField(
#         max_digits=7, decimal_places=2, null=True, blank=True)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     _id = models.AutoField(primary_key=True, editable=False)

#     def __str__(self):
#         return str(self.createdAt)

#     def __init__(self, *args, **kwargs):
#         super(self.__class__, self).__init__(*args, **kwargs)
        
#         self.total_price, self.final_price = self.update_price()  # check changes
#         self.__pre_discount = self.discount  # for check changed value in save method
#         self.__pre_status = self.status  # for check payment or canceling order
#         if self.status == 'U':
#             for item in self.items.all():  # remove items from order if count not enough
#                 if item.count > item.product.inventory: item.delete()
    
 

#     @property
#     def readable_total_price(self):
#         """
#         Make Readable Form of Total Price for Show in Template Pages
#         """

#         return readable(self.total_price)
    
#     @property
#     def readable_final_price(self):
#         """
#         Make Readable Form of Final Price for Show in Template Pages
#         """

#         return readable(self.final_price)
    
#     @property
#     def status_name(self):
#         """
#         Make Readable Form of Final Price for Show in Template Pages
#         """

#         return self.__class__.STATUSES[self.status]
    

# class OrderItem(models.Model):
#     class Meta:
#         verbose_name=" iسفارش "
#         verbose_name_plural =  " iسفارشات"
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     qty = models.IntegerField(null=True, blank=True, default=0)
#     price = models.DecimalField(
#         max_digits=7, decimal_places=2, null=True, blank=True)
#     image = models.CharField(max_length=200, null=True, blank=True)
#     _id = models.AutoField(primary_key=True, editable=False)

#     def __str__(self):
#         return str(self.name)        