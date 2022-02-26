from django.contrib import admin
from django.urls import path
app_name = 'product'

from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('about',about,name='about'),
    path('product',product,name='product'),
    path('why',why,name='why'),
    path('contact_us',contact_us,name='contact_us'),
    path('<slug:slug>/', product_detail, name='product_detail'),
    path('category/<slug:slug>/', product, name='category_filter'),
]