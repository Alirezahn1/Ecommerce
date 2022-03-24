from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['customer','city','province','description','home_plate','postal_code']