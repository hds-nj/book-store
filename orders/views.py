# from django.shortcuts import render , redirect
# from django.shortcuts import get_object_or_404
# from django.contrib import messages
# from .models import Product , ProductOrder , Cart
# # Create your views here.
# def add_to_cart(request,book_id):
#     book = get_object_or_404(Product, pk=book_id)
#     cart,created = Cart.objects.get_or_create(user=request.user, active=True)
#     order,created = BookOrder.objects.get_or_create(book=book,cart=cart)
#     order.quantity += 1
#     order.save()
#     messages.success(request, "Cart updated!")
#     return redirect('cart')