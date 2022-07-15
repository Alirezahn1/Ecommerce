
from django.urls import path
app_name = 'products'

from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('about/',AboutView.as_view(),name='about'),
    path('product/',ProductView.as_view(),name='product'),
    path('why/',WhyView.as_view(),name='why'),
    path('contact_us/',ContactUsView.as_view(),name='contact_us'),
    path('<str:prod_slug>/', productview, name='product_detail'),
    path('category/<slug:slug>/', ProductView.as_view(), name='category_filter'),



]