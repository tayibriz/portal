from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User


User = get_user_model()


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    requirements = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(default=None,max_length=100)  # Location of the job
    company_info = models.TextField(default=None)  # Information about the hiring company
    application_deadline = models.DateTimeField(default=datetime.now)  # Deadline for submitting applications
    job_type = models.CharField(default=None,max_length=50)  # Full-time, part-time, remote, etc.
    job_category = models.CharField(default=None,max_length=50)  # Category of the job (e.g., IT, Marketing, etc.)
    experience_level = models.CharField(default=None,max_length=50)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=100,default=None)
    email = models.EmailField(default=None)
    contact = models.CharField(max_length=20,default=None)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='doc', blank=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"




class Subscription(models.Model):
    SUBSCRIPTION_TYPES = [
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES)
    active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.recruiter.username} - {self.subscription_type} ({'Active' if self.active else 'Inactive'})"
    def upgrade_to_platinum(self):
        if self.subscription_type == 'gold':
            self.active = False
            self.subscription_type = 'platinum'
            self.active = True
            self.save()
    def set_expiration_date(self):
        if self.subscription_type == 'gold':
            self.expiration_date = datetime.now() + timedelta(days=30)  # 30 days for gold
        elif self.subscription_type == 'platinum':
            self.expiration_date = datetime.now() + timedelta(days=90)  # 90 days for platinum
        self.save()