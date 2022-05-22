from django.urls import path , include
from django.contrib.auth import views
from . import views 
from .views import *

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('password/', views.change_password, name="password"),
    path('edit-profile/' , UserEditView ,name='edit-profile'),
    path('account/', views.userAccount, name="account"),
    path('edit-account /', views.editAccount, name="edit-account"),
    path('', include('django.contrib.auth.urls')),
    ]