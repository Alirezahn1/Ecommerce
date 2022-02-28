from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from core.models import User
# Create your views here.
from django.views import View
from django.contrib import messages
from core.forms import UserCreationForm, UserLoginForm

from customers.models import Customer


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_register_info'] = {
                'email': cd['email'],
                'phone': cd['phone'],
                'first_name': cd['first_name'],
                'password': cd['password'],
                'last_name': cd['last_name'],
            }
            user = User.objects.create(email=cd['email'],phone=cd['phone'], first_name=cd['full_name'], last_name=cd['password'])
            user.save()
            messages.success(request, 'we sent you a code', 'success')
            return redirect('customers:login')
        return redirect('products:home')
    else:
        form = UserCreationForm()
    return render(request, 'customer/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('products:home')
            else:
                messages.error(request, 'username or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'customer/login.html', {'form': form})


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('products:home')
