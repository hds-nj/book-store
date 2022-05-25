from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    verbose_name="پروفایل"
    website = models.URLField(default='http://....com' , verbose_name="آدرس وب سایت")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile" , blank=True , null=True)
    birth_date = models.DateField(null=True, verbose_name= "تاریخ تولد",blank=True)
    email = models.EmailField(max_length=500, blank=True, null=True , verbose_name="ایمیل")
    def __str__(self):
        return str(self.user)
    def get_absolute_url(self):
        return reverse ('home') 

