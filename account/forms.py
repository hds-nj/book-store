from dataclasses import field
from pyexpat import model
from tkinter import Widget
from django.forms import *
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib.auth.models import User
from django import forms
from account.models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
class ProfilePageForm(forms.ModelForm):
    class Meta:           
     model = Profile
     fields = ('website' , 'birth_date' )
    
     widgets = {
      'website' : forms.TextInput(attrs={'class': 'form-control'}),
      'birth_date': forms.DateInput(attrs={'class': 'form-control'}),

     }

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.' )
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    class Meta:
        model = User
        fields = ['username','first_name',"last_name", 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

class EditProfileForm(UserChangeForm):
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name= forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50,widget= forms.TextInput(attrs={'class': 'form-control'}))
    # username = forms.CharField(max_length=100,widget= forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('first_name' , 'last_name' )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['website','birth_date','email' ] 
        def save(self , user=None):
            
            user_profile = super(ProfileUpdateForm , self).save(commite=False)
            if user:
                user_profile = user
            user_profile.save()
            return user_profile
   
class CustomerChangePassword(PasswordChangeForm):
    """
    Inheritanced from Built-in Change Password Form
    """

    pass            