from django.db import models
from core.models import BaseModel
# Create your models here.
from customers.models import Customer, Address
from products.models import Product, AbstractDiscount
from core.models import User

class OffCode(AbstractDiscount):
    code = models.CharField(max_length=15, unique=True)


class Order(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.RESTRICT,related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    off_code = models.ForeignKey(OffCode, on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.BooleanField(default=False)


    class Meta:
        unique_together = [['off_code', 'customer']]
        ordering = ('-created',)

    def __str__(self):
        return f'{self.customer} - {str(self.id)}'

    # def get_total_price(self):
    #     total = sum(item.get_cost() for item in self.items.all())
    #     if self.off_code:
    #         discount_price = (self.off_code / 100) * total
    #         return int(total - discount_price)
    #     return total

class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.price * self.amount

class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)