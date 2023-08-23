from django.urls import path
from .views import JobCreateView, JobListView, JobApplicationCreateView, JobApplicantsListView, SubscriptionCreateView, SubscriptionShowView,recommend_jobs

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:job_id>/applications/', JobApplicationCreateView.as_view(), name='job-application-create'),
    path('jobs/<int:job_id>/applicants/', JobApplicantsListView.as_view(), name='job-applicants-list'),
    path('subscription/create/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscription/show/', SubscriptionShowView.as_view(), name='subscription-show'),
    path('recommend/<int:user_id>/', recommend_jobs, name='recommend_jobs'),
   
    
]
