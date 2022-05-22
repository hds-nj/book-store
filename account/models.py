from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    verbose_name="پروفایل"
    website = models.URLField(default='')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile" , blank=True , null=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.user.username
      
def createProfile(sender, **kwargs):
         if kwargs['created']:
          user_profile = Profile.objects.created(user=kwargs['instance'])

         post_save.connect(createProfile, sender=User)
