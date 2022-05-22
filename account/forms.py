from dataclasses import field
from pyexpat import model
from tkinter import Widget
from django.forms import *
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib.auth.models import User
from django import forms
from account.models import Profile
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ['first_name',"last_name", 'email', 'birth_date','username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class EditProfileForm(UserChangeForm):
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name= forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50,widget= forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100,widget= forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name' )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date'] 
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']  
     
class EditProfileForm(forms.Form):
    class Meta:
        model = User
        fields = (
                 'email',
                 'first_name',
                 'last_name'
                )
               
    username = forms.CharField()
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def clean_username(self):
        """
        This function throws an exception if the username has already been 
        taken by another user
        """

        username = self.cleaned_data['username']
        if username != self.original_username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    'A user with that username already exists.')
        return username    
class CustomerChangePassword(PasswordChangeForm):
    """
    Inheritanced from Built-in Change Password Form
    """

    pass            