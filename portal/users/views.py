from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            



            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user using the provided username and password
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Perform login if the user is authenticated
        login(request, user)

        # Generate a new token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Perform login if the user is authenticated
        serializer = UserLoginSerializer(user)
        data = serializer.data
        data['token'] = access_token
        

        if user.role == 'admin':
            data['dashboard_url'] = '/admin-dashboard/'  # Replace with the admin dashboard URL
        elif user.role == 'user':
            data['dashboard_url'] = '/user-dashboard/'  # Replace with the user dashboard URL
        elif user.role == 'recruiter':
            data['dashboard_url'] = '/recruiter-dashboard/'  # Replace with the recruiter dashboard URL

               
        return Response(data, status=status.HTTP_200_OK)
        
