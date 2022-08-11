from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework.response import Response
from django.contrib import messages
from .models import *
from orders.forms import CartAddForm
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

class HomeView(View):
	def get(self,request):
		products = Product.objects.filter(available=True).exclude(discount=None)
		new_products= Product.objects.filter(trending=True)
		paginator = Paginator(new_products, 6)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request,'base/home.html',{'products': products,'new_products':new_products,'page_obj': page_obj})
class AboutView(View):
	def get(self,request):
		return render(request,'base/about.html',{})

class WhyView(View):
	def get(self,request):
		return render(request,'base/why.html',{})
class ContactUsView(View):
	def get(self,request):
		form = ContactForm()
		return render(request, 'base/contact_us.html', {'form': form})


class ProductView(View):
	def get(self,request,slug=None):
		products = Product.objects.filter(available=True)
		categories = Category.objects.filter(is_sub=False)
		paginator = Paginator(products, 6)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		if slug:
			category = get_object_or_404(Category, slug=slug)
			products = products.filter(category=category)
			paginator = Paginator(products, 6)
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)

		return render(request,'products/product.html',{'products': products, 'categories': categories,'page_obj': page_obj})



# class ProductDetailView(View):
# 	def get(self,request,slug):
# 		product = get_object_or_404(Product, slug=slug)
# 		form = CartAddForm()
# 		return render(request, 'products/product_detail.html', {'product':product,'form':form})

def productview(request,prod_slug):

	if (Product.objects.filter(slug=prod_slug)):
		product = Product.objects.filter(slug=prod_slug).first
		context = {'product':product}



	else:
		messages.error(request, 'no such product found')
		return redirect('products:product')



	return render(request,'products/product_detail.html',context)


from core.forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

@csrf_exempt
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			# subject = "Website Inquiry"
			# body = {
			# 	'first_name': form.cleaned_data['first_name'],
			# 	'last_name': form.cleaned_data['last_name'],
			# 	'email': form.cleaned_data['email_address'],
			# 	'message': form.cleaned_data['message'],
			# }
			# message = "\n".join(body.values())

			Contact.objects.create(first_name=form.cleaned_data['first_name'],last_name= form.cleaned_data['last_name']
											 ,email= form.cleaned_data['email'],message= form.cleaned_data['message'])
			messages.info(request, 'your message has been sent successfully!!')
			# try:
			#
			# 	# send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
			# 	messages.info(request, 'your message has been sent!!')
			# except BadHeaderError:
			# 	return HttpResponse('Invalid header found.')
			return redirect("products:home")

	form = ContactForm()
	return render(request, "base/contact_us.html", {'form': form})





