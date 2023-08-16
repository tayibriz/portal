from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from job.models import Subscription

# Custom UserAdmin class to display additional fields
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    fieldsets = (
        # ... existing fieldsets ...
        ('Additional Info', {
            'fields': (
                'profile_image', 'resume', 'profile_summary', 'key_skills',
                'employment_details', 'projects', 'it_skills', 'education',
                'accomplishments', 'certifications', 'personal_details', 'languages_known',
            ),
        }),
    )

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'subscription_type', 'active', 'expiration_date')


