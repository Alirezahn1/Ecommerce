from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.response import Response

from .models import *
from orders.forms import CartAddForm
from rest_framework.decorators import api_view
from .serializers import *


class HomeView(View):
	def get(self,request):
		products = Product.objects.filter(available=True).exclude(discount=None)
		new_products= Product.objects.all().order_by('id').reverse()[:6]
		return render(request,'base/home.html',{'products': products,'new_products':new_products})
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
		paginator = Paginator(products, 3)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		if slug:
			category = get_object_or_404(Category, slug=slug)
			products = products.filter(category=category)
			paginator = Paginator(products, 3)
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)

		return render(request,'products/product.html',{'products': products, 'categories': categories,'page_obj': page_obj})



class ProductDetailView(View):
	def get(self,request,slug):
		product = get_object_or_404(Product, slug=slug)
		form = CartAddForm()
		return render(request, 'products/product_detail.html', {'product':product,'form':form})

@api_view(['POST'])
def search(request):
	query = request.data.get('query','')
	if query:
		products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontain=query))
		serializer = ProductSerializer(products,many=True)
		return Response(serializer.data)
	else:
		return Response({"products":[]})