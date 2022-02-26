from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import *

class HomeView(View):
    def get(self,request):
        return render(request,'base/home.html',{})
class AboutView(View):
    def get(self,request):
        return render(request,'base/about.html',{})

class WhyView(View):
    def get(self,request):
        return render(request,'base/why.html',{})
class ContactUsView(View):
    def get(self,request):
        return render(request, 'base/contact_us.html', {})


class ProductView(View):
    def get(self,request,slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)

        return render(request,'products/product.html',{'products': products, 'categories': categories})



class ProductDetailView(View):
    def get(self,request,slug):
	    product = get_object_or_404(Product, slug=slug)
	    return render(request, 'products/product_detail.html', {'product':product})
