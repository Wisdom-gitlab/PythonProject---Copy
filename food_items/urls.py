from django.urls import path
from . import views

urlpatterns=[
    path('',views.home_view, name='home'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('register/',views.register_view, name='register'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('about/', views.about, name='about')


]

