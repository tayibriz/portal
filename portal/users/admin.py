from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Custom UserAdmin class to display additional fields
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
