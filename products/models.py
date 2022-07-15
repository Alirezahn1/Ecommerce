from django.db import models
from django.urls import reverse

from core.models import *
# Create your models here.

class AbstractDiscount(BaseModel):
    value = models.PositiveIntegerField(null=False)
    type = models.CharField(max_length=10, choices=[('price', 'Price'), ('percent', 'Percent')], null=False)
    max_price = models.PositiveIntegerField(null=True, blank=True)

    def profit_value(self, price: int):
        """
        Calculate and Return the profit of the discount
        :param price: int (item value)
        :return: profit
        """
        if self.type == 'price':
            return min(self.value, price)
        else:  # percent
            raw_profit = int((self.value / 100) * price)
            return int(min(raw_profit, int(self.max_price))) if self.max_price else raw_profit

    class Meta:
        abstract = True


class Discount(AbstractDiscount):
	def __str__(self):
		return f'{self.type} , {self.value}'

class Category(BaseModel):
	sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
	is_sub = models.BooleanField(default=False)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = ('category')
		verbose_name_plural = ('categories')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('products:category_filter', args=[self.slug,])


class Product(BaseModel):
	category = models.ManyToManyField(Category, related_name='products')
	name =  models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d/')
	description = models.TextField()
	price = models.IntegerField()
	available = models.BooleanField(default=True)
	discount = models.ForeignKey(to=Discount, on_delete=models.SET_NULL, null=True,blank=True)
	quantity = models.IntegerField(null=False,blank=False)
	tag = models.CharField(max_length=200,null=True,blank=True)
	trending = models.BooleanField(default=False,help_text='1 = Trending')



	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('products:product_detail', args=[self.slug,])

	def final_price(self):
		if self.discount.type == 'percent':
			return int(self.price - ((self.discount.value/100)*self.price))
		else:
			return self.price - self.discount.value

class Wishlist(BaseModel):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
