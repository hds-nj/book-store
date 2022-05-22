from multiprocessing import context
from django.urls import path 

from .views import  *
app_name = "products"
urlpatterns = [
    path('shop/', shop , name="shop"),
    path('<slug:slug>', Product, name="detail"),
    # path('shop/' , ProductPreviw.as_view , name="shop"),
    # path('preview/<int:pk>', ProductPreviw.as_view() , name="preview"),
    path('category/<slug:slug>' , category , name="ProCategory" ),
    # path('', products, name = "products"),
    # path('add/<int:book_id>', add_to_cart, name='add_to_cart'),    
    # path('remove/<int:book_id>', remove_from_cart, name='remove_from_cart'), 
    # path('cart/', cart, name='cart'),
    path('cart/', checkout, name="checkout"),
    path('remove/', remove, name="remove"),
    path('remove_all/', remove_all, name="remove_all"),
    path('add/', add, name="add"),
    path('buy/', buy, name="buy"),

]