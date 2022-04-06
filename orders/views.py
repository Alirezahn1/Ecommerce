from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from .models import Orderitem


# Create your views here.


class OrderItemDetailView(ListView):
    template_name = 'orders/items.html'
    model = Orderitem
    context_object_name = 'items'

    def get_queryset(self):
        return Orderitem.objects.filter(order__customer__user=self.request.user)


# def updateItem(request):
#     return JsonResponse('it was added',safe=False)