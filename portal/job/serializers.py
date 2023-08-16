from rest_framework import serializers
from .models import Job, JobApplication,Subscription

class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.ReadOnlyField(source='recruiter.id')
    class Meta:
        model = Job
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscription_type']



class SubscriptionSerializer(serializers.ModelSerializer):
    recruiter = serializers.ReadOnlyField(source='recruiter.id')
    class Meta:
        model = Subscription
        fields = '__all__'