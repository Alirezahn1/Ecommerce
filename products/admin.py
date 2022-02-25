from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Discount)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}

