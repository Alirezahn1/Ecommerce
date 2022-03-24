
from rest_framework import serializers
from .models import *

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderitem
        fields = ['product','order','amount']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderitem
        fields = ['customer','address','off_code','paid']

