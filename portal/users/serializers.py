from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'profile_image', 'resume', 'profile_summary', 'skills',
                  'employment_details', 'projects', 'education', 'accomplishments',
                  'certifications', 'personal_details', 'languages_known']
        

class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'profile_image', 'contact_info','employment_details', 'skills','recruitment_specialities','education',
                  'certifications', 'personal_details', 'languages_known','social_media_links','client_company_list']


