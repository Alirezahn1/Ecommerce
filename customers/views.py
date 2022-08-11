
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from core.models import User
# Create your views here.
from django.views import View
from django.contrib import messages
from core.forms import UserCreationForm, UserLoginForm, UserChangeForm

from customers.models import Customer


class UserRegisterView(View):
    def post(self,request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                customer = Customer.objects.create(user=user)
                customer.save()
                messages.success(request, 'successfully registered', 'success')
                return redirect('customers:login')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('customers:register')
    def get(self,request):
        form = UserCreationForm()
        return render(request, 'customer/register.html', {'form': form})


class UserLoginView(View):
    def post(self,request):
        if request.method == 'POST':
            form = UserLoginForm(request.POST)

            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, phone=cd['phone'], password=cd['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You logged in successfully', 'success')
                    return redirect('products:home')
                else:

                    messages.error(request, 'phone or password is wrong', 'danger')
                    return redirect('customers:login')
    def get(self,request):
        if request.user.is_authenticated:
            messages.warning(request,'You are already logged in !!')
            return redirect('products:home')
        else:
            form = UserLoginForm()
            return render(request, 'customer/login.html', {'form': form})



class UserLogoutView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def get(self,request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('products:home')

from django.views import generic

class UserEditView(LoginRequiredMixin,generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    form_class = UserChangeForm
    template_name = 'customer/profile.html'
    success_url = reverse_lazy('products:home')

    def get_object(self, queryset=None):
        return self.request.user

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('products:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'customer/changepassword.html', {
        'form': form
    })
