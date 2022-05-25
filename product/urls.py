from multiprocessing import context
from django.urls import path 
from . import views
from .views import  *
app_name = "products"
urlpatterns = [
    path('shop/', shop , name="shop"),
    path('<slug:slug>', views.product , name="detail"),
    path('category/<slug:slug>' , views.category , name="Category" ),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update-item/',views.updateItem , name="update-item")

]