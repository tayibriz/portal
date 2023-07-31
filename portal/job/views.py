from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class JobListView(APIView):
    def get(self, request):
        if request.user.role == 'recruiter':
            jobs = Job.objects.filter(recruiter=request.user)
        else:
            jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
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
