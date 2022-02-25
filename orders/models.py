from django.db import models
from core.models import BaseModel
# Create your models here.
from customers.models import Customer, Address
from products.models import Product, AbstractDiscount


class OffCode(AbstractDiscount):
    code = models.CharField(max_length=15, unique=True)


class Order(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.RESTRICT)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    off_code = models.ForeignKey(OffCode, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = [['off_code', 'customer']]