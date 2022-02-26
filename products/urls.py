
from django.urls import path
app_name = 'product'

from .views import *
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('about',AboutView.as_view(),name='about'),
    path('product',product,name='product'),
    path('why',WhyView.as_view(),name='why'),
    path('contact_us',ContactUsView.as_view(),name='contact_us'),
    path('<slug:slug>/', product_detail, name='product_detail'),
    path('category/<slug:slug>/', product, name='category_filter'),
]