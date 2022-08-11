from django.contrib import admin

# Register your models here.
from customers.models import *

admin.site.register(Customer)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer','province','city','description')
    search_fields = ('province', 'city', 'customer')
    ordering = ('customer',)