from django import forms
from .models import User, Contact
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from .validators import check_phone


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password again'}))

    class Meta:
        model = User
        fields = ('phone','email','first_name','last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'email form-control my-2','placeholder':'Enter your Email'}),
            'phone' : forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder ': 'Enter your phone'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter your last name'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords must match')
        return cd['password2']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return check_phone(phone)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name','last_name','phone','email',)
        widgets = {

            'email': forms.EmailInput(attrs={'class': 'email form-control my-2', 'placeholder': 'Enter your Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter your last name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder ': 'Enter your phone'}),
        }


class UserLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-3','placeholder':'Enter your phone'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-3','placeholder':'Enter your password'}))
    # class Meta:
    # 	model = User
    # 	fields = ('phone','password')

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length = 50,widget=forms.TextInput(attrs={'class': 'form-control my-2 required', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length = 50,widget=forms.TextInput(attrs={'class': 'form-control my-2 required', 'placeholder': 'Enter your last name'}))
    email = forms.EmailField(max_length = 150,widget=forms.EmailInput(attrs={'class': 'email form-control my-2 required','placeholder':'Enter your Email'}))
    message = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control my-2 required', 'placeholder ': 'Enter your message'}), max_length = 2000)

    class Meta:
        model = Contact
        fields = ('first_name','last_name','email','message')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'email form-control my-2','placeholder':'Enter your Email'}),
            'message' : forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder ': 'Enter your message'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter your last name'}),
        }
