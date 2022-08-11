
from django.db import models

# Create your models here.
from core.models import User, BaseModel


class Customer(BaseModel):
    user = models.OneToOneField(User, models.CASCADE,primary_key=True )

    def __str__(self):
        return self.user.phone

class Address(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    home_plate = models.CharField(max_length=3)
    postal_code = models.CharField(max_length=10,help_text='Enter 10 digits')

    class Meta:
        verbose_name_plural = ('addresses')


    def __str__(self):
        return self.customer.user.phone