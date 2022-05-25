
from django.http import JsonResponse
from django.shortcuts import render, redirect ,get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Product , Category , Order 
from account.models import Profile
from django.contrib.auth.models import User
from .models import Profile
import json

# Create your views here.
def home (request):
    category = Category.objects.all()
    products=Product.objects.all()
    if request.user.is_authenticated:
       user = request.user
       order, created = Order.objects.get_or_create(customer=user , complete=False)
       items = order.orderitem_set.all()
       cartItem = order.get_cart_items
    else:
       items = [] 
       order = {'get_card_total':0 ,'get_cart_items':0}
       cartItem = order['get_cart_items']
    
    return render(request, "index.html" , {'category':category ,'products':products,'cartItem':cartItem ,'items':items})
def shop(request , page=1):
        if request.user.is_authenticated:
           user = request.user
           order, created = Order.objects.get_or_create(customer=user , complete=False)
           items = order.orderitem_set.all()
           cartItem = order.get_cart_items
        else:
            items = [] 
            order = {'get_card_total':0 ,'get_cart_items':0}
            cartItem = order['get_cart_items']
            
        products=Product.objects.all()
        paginator =Paginator(products,4)
        productsList = paginator.get_page(page)
        context={
           'products':products ,'productsList':productsList ,'cartItem':cartItem ,'items':items
        }
        return render(request,"books/shop.html",context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        order = {'get_card_total':0 ,'get_cart_items':0}
        items = []    
    context ={'items':items , 'order':order , 'cartItem':cartItem}
    return render(request , 'books/cart.html' , context )       

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
    else:
        items = []    
    context ={'items':items}
    return render(request , 'books/checkout.html' , context )     


@login_required(login_url='login')

def updateItem(request):
    decoded_data = request.body.decode('utf-8')
    data = json.loads(decoded_data)
    productId = data['productId']
    action = data['action']
    print('Action:' , action)
    print('Product:', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created =Order.objects.get_or_create(customer=customer , complete = False)
    orderItem,created = OrderItem.objects.get_or_create(order = order , product = product)
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save() 
    if orderItem.quantity <= 0:
        orderItem.delete()   
    return JsonResponse('Item was added' , safe =False)


def product(request , slug):  
       context= {
           "product" : Product.objects.get(slug=slug),
           "category" : Category.objects.all()
       }
       return render (request , "books/product.html" , context )


def category(request , slug):
    context = {
        "category" : get_object_or_404( Category , slug=slug )
    }
    return render(request , "books/book-category.html" , context)








# def add_to_cart(request, product_id):
#     if request.user.is_authenticated:
#         try: 
#             product = Product.objects.get(pk=product_id)
#         except ObjectDoesNotExist:
#             pass
#         else:
#             try:
#                 cart = Cart.objects.get(user=request.user, active=True)
#             except ObjectDoesNotExist:
#                 cart = Cart.objects.create(
#                     user=request.user
#                 )
#                 cart.save()
#             cart.add(product , product_id)
#         return redirect('cart')
#     else:
#         return redirect('home')


# def remove_from_cart(request, book_id):
#     if request.user.is_authenticated:
#         try:
#             book = Product.objects.get(pk=book_id)
#         except ObjectDoesNotExist:
#             pass
#         else:
#             cart = Cart.objects.get(user=request.user, active=True)
#             cart.remove_from_cart(book_id)
#         return redirect('cart')
#     else:
#         return redirect('home')

# def cart(request):
#     if request.user.is_authenticated:
#         cart = Cart.objects.get(user=request.user.id, active=True)
#         orders = Order.objects.filter(cart=cart)
#         total = 0
#         count = 0
        
#         for order in orders:
#             total += (order.book.price * order.quantity)
#             count += order.quantity
        
#         context = {
#             'cart': orders, 
#             'total': total,
#             'count': count,
#         }
#         return render(request, 'cart.html', context)
#     else:
#         return redirect('home')

# class ProductPreviw(DetailView):
#     template_name = "books/product.html"
#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         return get_object_or_404(Product, pk=pk)

# class ProductsListView(generic.ListView):

#     context_object_name = "products"

#     def get_queryset(self): 
#         kwargs = self.request.GET
#         if "category" in kwargs:
#             result = result.filter(category__slug=kwargs["category"])
#         return Product.objects.all()

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context.update({
#     #         'slides': Product.objects.exclude(image='Unknown.jpg').order_by('?')[:3],
#     #     })
        
#     #     return context


# class ProductDetailView(generic.DetailView):
#     model = Product
#     context_object_name = "product"

#     def post(self, request, *args, **kwargs):
#         resp = JsonResponse({'msg': ("Product Item has Successfully been Added to the Cart")})
#         cart = request.COOKIES.get("cart", "")
#         resp.set_cookie("cart", cart + request.POST["product"] + ',')
#         context={"resp":resp}
#         return render(request , context , 'books/product.html') 
