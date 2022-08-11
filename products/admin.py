from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug','is_sub','sub_category')
	prepopulated_fields = {'slug': ('name',)}
	list_filter = ('is_sub',)
	search_fields = ('name',)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'available','discount','quantity','trending')
	list_filter = ('available','discount')
	list_editable = ('price',)
	prepopulated_fields = {'slug': ('name',)}
	raw_id_fields = ('category',)
	actions = ('make_available',)
	search_fields = ('name','category','description',)
	def make_available(self, request, queryset):
		rows = queryset.update(available=True)
		self.message_user(request, f'{rows} updated')
	make_available.short_description = 'make all available'

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
	list_display = ('value', 'type','max_price')
	list_filter = ('type',)
	search_fields = ('value',)