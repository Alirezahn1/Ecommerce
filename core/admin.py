from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User



class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('date_joined', 'email','phone', 'is_staff','is_superuser')
	list_filter = ('is_staff','is_active','is_superuser')
	fieldsets = (
		('Main', {'fields':('first_name','last_name','email','phone', 'password')}),
		('Personal info', {'fields':('is_active','date_joined',)}),
		('Permissions', {'fields':('is_staff','is_superuser',)})
	)
	add_fieldsets = (
		('Main', {
			'fields':('first_name','last_name', 'email','phone', 'password1', 'password2','is_staff','is_superuser')
		}),
	)
	search_fields = ('email','phone','first_name','last_name',)
	ordering = ('date_joined',)

admin.site.register(User, UserAdmin)