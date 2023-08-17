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
    recruiter_username = serializers.CharField(source='recruiter.username', read_only=True)
    recruiter = serializers.ReadOnlyField(source='recruiter.id')
    subscription_status = serializers.BooleanField(source='active', read_only=True)
    jobs_left = serializers.SerializerMethodField()
    class Meta:
        model = Subscription
        fields = '__all__'
    def get_jobs_left(self, subscription):
        # Adjust this logic based on your subscription rules and job posting limits
        posted_jobs_count = Job.objects.filter(recruiter=subscription.recruiter).count()
        if subscription.subscription_type == 'gold':
            jobs_left = 10 - posted_jobs_count
            return max(jobs_left, 0)
        elif subscription.subscription_type == 'platinum':
            jobs_left = 20 - posted_jobs_count
            return max(jobs_left, 0)  # Ensure it's not negative
        return 0
    