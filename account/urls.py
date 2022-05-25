from django.urls import path , include
from django.contrib.auth import views
from . import views 
from .views import *

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('password/', views.change_password, name="password"),
    path('', include('django.contrib.auth.urls')),
    path('edit/<pk>', EditProfileView.as_view(), name="edit-user-profile"),
    path('<int:pk>/profile' , ShowProfilePageView.as_view(), name = "show-profile-page"),
    ]