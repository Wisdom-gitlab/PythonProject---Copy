from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Product, Category, Cart, CartItem,Order, OrderItem

# Create your views here.


def register_view(request):
    if request.method=="POST":
        form=RegisterForm(request.POST )
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=User.objects.create_user(username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
            form=RegisterForm()
    return render(request,'accounts/register.html',{'form':form})
        

def login_view(request):
    error_message=None
    if request.method=="POST":
      username=request.POST.get("username")
      password=request.POST.get("password")
      user=authenticate(request,username=username,password=password)
      if user is not None:
          login(request,user) 
          next_url=request.POST.get('next') or request.GET.get('next') or 'home'
          return redirect(next_url)
      else:
          error_message="Invalid Credentials !"
    return render(request,'accounts/login.html',{'error':error_message})

def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

@login_required

def home_view(request):
    categories = Category.objects.all()
    data = []

    for category in categories:
        products = Product.objects.filter(category=category)
        data.append({
            'category': category,
            'products': products
        })

    return render(request, 'auth1/index.html', {'data': data})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'auth1/product_detail.html', {'product': product})

def get_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()

    cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = get_cart(request)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = get_cart(request)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')
def cart_view(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.total_price() for item in items)

    return render(request, 'auth1/cart.html', {
        'items': items,
        'total': total
    })

def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id)
    item.delete()
    return redirect('cart')

def search(request):
    query = request.GET.get('q')
    products = []

    if query:
        products = Product.objects.filter(name__icontains=query)

    return render(request, 'auth1/search.html', {
        'products': products,
        'query': query
    })




def checkout(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect('cart')

    total = sum(item.total_price() for item in items)

    order = Order.objects.create(
        session_id=cart.session_id,
        total_price=total
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    items.delete()

    return redirect('success')


def success(request):
    return render(request, 'auth1/success.html')

def about(request):
    return render(request, 'auth1/about.html')









