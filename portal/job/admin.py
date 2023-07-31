from django.contrib import admin
from .models import  Job, JobApplication
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'created_at')
    list_filter = ('recruiter',)
    search_fields = ('title', 'recruiter__username', 'recruiter__email')

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'email', 'contact', 'applied_at','resume')
    list_filter = ('job__recruiter', 'job')
    search_fields = ('name', 'email', 'job__title', 'job__recruiter__username', 'job__recruiter__email')
    


admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)