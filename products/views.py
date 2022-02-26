from django.shortcuts import render, get_object_or_404
from .models import *

def home(request):
    return render(request,'base/home.html',{})
def about(request):
    return render(request,'base/about.html',{})

def why(request):
    return render(request,'base/why.html',{})
def contact_us(request):
    return render(request, 'base/contact_us.html', {})


def product(request,slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.filter(is_sub=False)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

    return render(request,'products/product.html',{'products': products, 'categories': categories})



def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	return render(request, 'products/product_detail.html', {'product':product})
