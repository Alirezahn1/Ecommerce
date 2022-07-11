
from django.urls import path
from .views import *


app_name = 'orders'



urlpatterns = [
    path('add-to-cart/',addtocart,name='addtocart'),
    path('cart/', viewcart, name='cart'),

]