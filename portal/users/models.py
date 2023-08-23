from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('recruiter','Recruiter'),
    )
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    

    #userprofile
    first_name=models.CharField(max_length=20,blank=True)
    last_name=models.CharField(max_length=20,blank=True)

    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    profile_summary = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    employment_details = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    education = models.TextField(blank=True)
    accomplishments = models.TextField(blank=True)
    certifications = models.URLField(blank=True)
    personal_details = models.TextField(blank=True)
    languages_known = models.TextField(blank=True)

    contact_info = models.TextField(blank=True)
    recruitment_specialities = models.TextField(blank=True)
    client_company_list = models.TextField(blank=True)
    social_media_links = models.TextField(blank=True)

    def __str__(self):
        return self.username