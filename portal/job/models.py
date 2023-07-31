from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    requirements = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)

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
