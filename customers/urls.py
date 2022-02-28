
from django.urls import path


from .views import *
app_name = 'customers'

urlpatterns = [
    path('register/',register,name='register'),
    path('login/', login_user, name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]