from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from products.models import Product, Wishlist
from .models import *
from customers.urls import *

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id):
                    return JsonResponse({'status': "Product Already in Cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product Added successfully"})
                    else:
                        return JsonResponse({'status': "Only  " + str(product_check.quantity) + "quantity available"})
            else:
                return JsonResponse({'status': "No such product found"})


        else:
            return JsonResponse({'status': "login to Continue"})

    return redirect('products:home')


@login_required(login_url='customers:login')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart': cart}
    return render(request, 'orders/cart.html', context)


@csrf_exempt
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': "Updated Successfully"})
    return redirect('products:home')


@csrf_exempt
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status': "Deleted Successfully"})
    return redirect('products:home')


@csrf_exempt
def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Wishlist.objects.filter(user=request.user, product_id=prod_id):
                    return JsonResponse({'status': "Product Already in Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product Added to Wishlist"})


            else:
                return JsonResponse({'status': "No such product found"})

        else:
            return JsonResponse({'status': "login to Continue"})

    return redirect('products:home')

@login_required(login_url='customers:login')
def wishlistview(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context ={'wishlist':wishlist}
    return render(request,'products/wishlist.html',context)

@csrf_exempt
def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if Wishlist.objects.filter(user=request.user, product_id=prod_id):
                whishitem = Wishlist.objects.get(product_id=prod_id, user=request.user)
                whishitem.delete()
                return JsonResponse({'status': "Product removed from Wishlist Successfully"})
            else:
                return JsonResponse({'status': "Product not found in wishlist"})
        else:
            return JsonResponse({'status': "login to Continue"})
    return redirect('products:home')

@login_required(login_url='customers:login')
def checkout(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        if item.product.discount:
            total_price = total_price + item.product.final_price() * item.product_qty
        else:
            total_price = total_price + item.product.price * item.product_qty


    context = {'cartitems':cartitems,'total_price':total_price}
    return render(request,'orders/checkout.html',context)

@login_required(login_url='customers:login')
@csrf_exempt
def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        customer = Customer.objects.get(user=request.user)
        neworder.customer = customer
        newaddress =Address.objects.create(customer=customer,city=request.POST.get('city'),province=request.POST.get('province')
                                           ,description=request.POST.get('address'),home_plate=request.POST.get('plate')
                                           ,postal_code=request.POST.get('code'))
        neworder.address = newaddress
        cart = Cart.objects.filter(user=request.user)
        total_price = 0
        for item in cart:
            if item.product.discount:
                total_price = total_price + item.product.final_price() * item.product_qty
            else:
                total_price = total_price + item.product.price * item.product_qty

        neworder.total_price = total_price
        neworder.paid = True
        neworder.save()
        neworderitem = Cart.objects.filter(user=request.user)
        for item in neworderitem :
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                quantity=item.product_qty
            )
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        Cart.objects.filter(user=request.user).delete()
        messages.success(request, 'your order has been placed successfully')

    return redirect('products:home')


def myorders(request):
    customers = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customers)
    context = {'orders': orders}
    return render(request,'orders/myorders.html',context)

def orderview(request,pk):
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.filter(customer=customer).filter(id=pk).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order,'orderitems':orderitems}
    return render(request,'orders/view.html',context)

def productlist(request):
    products = Product.objects.filter(available=True).values_list('name',flat=True)
    productslist = list(products)
    return JsonResponse(productslist,safe=False)

@csrf_exempt
def searchproduct(request):
    if request.method == 'POST':
        searched = request.POST.get('productsearch')
        if searched == '':
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains= searched).first()
            if product:
                return redirect(product.get_absolute_url())
            else:
                messages.info(request,'No product matched your search')
                return redirect(request.META.get('HTTP_REFERER'))


    return redirect(request.META.get('HTTP_REFERER'))
