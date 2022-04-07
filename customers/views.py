from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
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
                # cd = form.cleaned_data
                # email= cd['email']
                # phone= cd['phone']
                # first_name= cd['first_name']
                # password1= cd['password1']
                # last_name= cd['last_name']
                # password2= cd['password2']
                #
                # user = User.objects.create(email=email,phone=phone, first_name=first_name, last_name=last_name,password=password1)
                # user.save()

                user = form.save(commit=False)
                user.save()
                customer = Customer.objects.create(user=user)
                customer.save()
                messages.success(request, 'successfully registered', 'success')
                return redirect('customers:login')
            else:
                messages.error(request,form.errors,'danger')
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

