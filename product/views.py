
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from urllib import request
from .models import Product , Category , Cart , CartItem
from account.models import Profile
from django.shortcuts import render, get_object_or_404 , redirect
# Create your views here.
def home (request):
    return render(request, "index.html")

def shop(request , page=1):
       products=Product.objects.all()
       paginator =Paginator(products,4)
       productsList = paginator.get_page(page)
       context={
           'products':products ,'productsList':productsList
       }
       return render(request,"books/shop.html",context)
       
def product(request , slug):  
       context= {
           "product" : Product.objects.get(slug =slug ),
           "category" : Category.objects.all()
       }
       return render (request , "books/product.html" , context )


def category(request , slug):
    context = {
        "category" : get_object_or_404( Category , slug=slug )
    }
    return render(request , "books/book-category.html" , context)

@login_required(login_url='login')
def checkout(request):
    if request.method == 'GET':
        _cart = dict()
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        if len(cart) > 0:
            cart_items = CartItem.objects.filter(cart=cart[0])[::1]
            total = sum([cart_item.quantity * cart_item.good.price for cart_item in cart_items])
            discount = total - cart[0].total
            cart_total = cart[0].total + 50
            _cart['total'] = total
            _cart['discount'] = discount
            _cart['cart_total'] = cart_total
        else:
            cart_items = []
    else:
        cart_items = []
    goods = Product.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, 'checkout.html', {'cart_items': cart_items, 'goods': goods, 'categories': categories, 'cart': _cart})

@login_required(login_url='login')
@csrf_protect
def remove(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        if len(cart) > 0:
            item = CartItem.objects.get(id=request.POST.get('id'))
            item.cart.total -= item.quantity * item.good.price
            item.cart.save()
            if item is not None:
                item.delete()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@login_required(login_url='login')
@csrf_protect
def remove_all(request):
    if request.method == "GET" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        if len(cart) > 0:
            for item in CartItem.objects.filter(cart=cart[0]):
                item.delete()
            cart[0].total = 0
            cart.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest()

@login_required(login_url='login')
def add(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        cartItem = CartItem()
        if len(cart) > 0:
            cartItem.cart = cart[0]
        else:
            cart = Cart()
            cart.profile = profile
            cart.total = 0.0
            cart.save()
            cartItem.cart = cart
        cartItem.quantity = int(request.POST.get('id_quantity'))
        cartItem.material = request.POST.get('id_material')
        cartItem.good = Product.objects.get(id=request.POST.get('id_good_id'))
        cartItem.save()
        return redirect('/good/{0}'.format(request.POST.get('id_good_id')))
    else:
        return HttpResponseBadRequest()

@login_required(login_url='login')
def buy(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))[0]
        cart.is_active = False
        cart.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest()






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
