
from django.urls import path
from .views import *
from .apis import *

app_name = 'orders'



urlpatterns = [
    path('order/<int:pk>', OrderItemApi.as_view(),name ='order'),
    path('cart/', OrderItemDetailView.as_view(), name='cart'),
    path('orderitem/<int:pk>', OrderItemDetailApi.as_view(), name='order_item'),
    # path('update_item/', updateItem, name='update_item'),

]