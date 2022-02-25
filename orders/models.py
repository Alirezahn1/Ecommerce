from django.db import models
from core.models import BaseModel
# Create your models here.
from customers.models import Customer, Address
from products.models import Product, AbstractDiscount


class OffCode(AbstractDiscount):
    code = models.CharField(max_length=15, unique=True)
