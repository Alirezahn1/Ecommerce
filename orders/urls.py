
from django.urls import path
from .views import *


app_name = 'orders'



urlpatterns = [
    path('add-to-cart/',addtocart,name='addtocart'),
    path('cart/', viewcart, name='cart'),
    path('update-cart/',updatecart,name='updatecart'),
    path('delete-cart-item/',deletecartitem,name='deletecartitem'),
    path('add-to-wishlist/', addtowishlist, name='addtowishlist'),
    path('wishlist', wishlistview, name='wishlist'),
    path('delete-wishlist-item/',deletewishlistitem,name='deletewishlistitem'),
    path('checkout', checkout, name='checkout'),
    path('place-order', placeorder, name='placeorder'),
    path('my-orders', myorders, name='myorders'),
    path('orderview/<str:pk>/', orderview, name='orderview'),
]