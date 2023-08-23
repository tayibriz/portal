from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from job.models import Subscription

# Custom UserAdmin class to display additional fields
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Adding a new user
            fieldsets = super().get_fieldsets(request, obj)
            return fieldsets
        
        if obj.role == 'recruiter':
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
                ('Recruiter Info', {'fields': ('contact_info', 'recruitment_specialities', 'social_media_links', 'client_company_list')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                ('Important dates', {'fields': ('last_login', 'date_joined')}),
            )
        else:
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
                ('User Info', {'fields': ('profile_image', 'resume', 'profile_summary', 'skills', 'employment_details', 'projects', 'education', 'accomplishments', 'certifications', 'personal_details', 'languages_known')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                ('Important dates', {'fields': ('last_login', 'date_joined')}),
            )
        
        return fieldsets

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'subscription_type', 'active', 'expiration_date')


