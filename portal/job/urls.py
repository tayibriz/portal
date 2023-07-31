from django.urls import path
from .views import JobCreateView, JobListView, JobApplicationCreateView, JobApplicantsListView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:job_id>/applications/', JobApplicationCreateView.as_view(), name='job-application-create'),
    path('jobs/<int:job_id>/applicants/', JobApplicantsListView.as_view(), name='job-applicants-list'),
]
