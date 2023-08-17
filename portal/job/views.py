import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer, SubscriptionSerializer 
from .serializers import SubscriptionCreateSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from datetime import datetime,date,timedelta
from .models import Subscription
from django_filters import rest_framework as filters
from .filters import JobFilter 




class JobCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recruiter = request.user

        job_count = Job.objects.filter(recruiter=recruiter).count()

        if job_count == 0:
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(recruiter=recruiter)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:

        # Check if the recruiter has an active subscription
            subscription_check_result = self.check_recruiter_subscription(recruiter)
            if subscription_check_result['allowed']:
                serializer = JobSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(recruiter=recruiter)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(subscription_check_result['error'], status=status.HTTP_403_FORBIDDEN)

    def check_recruiter_subscription(self, recruiter):
        try:
            subscription = Subscription.objects.get(recruiter=recruiter)
            if subscription.active:
                expiration_date = subscription.expiration_date.date()
                today=date.today()
                if expiration_date >= today:
                    job_limit=0
                    if subscription.subscription_type == 'gold':
                        job_limit = 10
                    elif subscription.subscription_type == 'platinum':
                        job_limit = 15


                    jobs_posted = Job.objects.filter(recruiter=recruiter, created_at__gte=expiration_date - timedelta(days=30)).count()
                    if jobs_posted < job_limit:
                        return {'allowed': True}
                    else:
                        return {'allowed': False, 'error': {'error': f'You have exceeded the maximum allowed jobs for your subscription type ({subscription.subscription_type}).'}}
                else:
                    return {'allowed': False, 'error': {'error': 'Your subscription has expired. Please renew your subscription.'}}
            else:
                return {'allowed': False, 'error': {'error': 'Your subscription is not active. Please activate your subscription.'}}
        except Subscription.DoesNotExist:
            return {'allowed': False, 'error': {'error': 'You need an active subscription to post jobs.'}}
    

class JobListView(APIView):
    def get(self, request):
        if request.user.role == 'recruiter':
            jobs = Job.objects.filter(recruiter=request.user)
        else:
            jobs = Job.objects.all()
        job_filter = JobFilter(request.GET, queryset=jobs)
        serializer = JobSerializer(job_filter.qs, many=True)  # Use filtered queryset
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobApplicationCreateView(APIView):
    def post(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save(job=job)  # Associate the application with the specific job
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobApplicantsListView(APIView):
    def get(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        if request.user == job.recruiter:
            applicants = job.jobapplication_set.all()
            serializer = JobApplicationSerializer(applicants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


#subscription
class SubscriptionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionCreateSerializer

    def get_existing_subscription(self):
        user = self.request.user
        try:
            return Subscription.objects.get(recruiter=user)
        except Subscription.DoesNotExist:
            return None

    def perform_create(self, serializer):
        existing_subscription = self.get_existing_subscription()
        
        if existing_subscription:
            existing_subscription.upgrade_to_platinum()
            existing_subscription.subscription_type = serializer.validated_data.get('subscription_type')
            existing_subscription.active = True
            existing_subscription.save()
        else:
            new_subscription = serializer.save(recruiter=self.request.user)
            new_subscription.set_expiration_date()

class SubscriptionShowView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_object(self):
        user = self.request.user
        try:
            return Subscription.objects.get(recruiter=user)
        except Subscription.DoesNotExist:
            return None