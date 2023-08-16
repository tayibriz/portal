import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    job_type = django_filters.CharFilter(field_name='job_type', lookup_expr='iexact')
    job_category = django_filters.CharFilter(field_name='job_category', lookup_expr='iexact')
    experience_level = django_filters.CharFilter(field_name='experience_level', lookup_expr='iexact')

    class Meta:
        model = Job
        fields = ['location', 'job_type', 'job_category', 'experience_level']
