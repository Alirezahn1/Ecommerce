
from django.urls import path


from .views import *
app_name = 'customers'

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserEditView.as_view(), name='profile'),
    path('changepassword/', change_password, name='changepassword'),

]