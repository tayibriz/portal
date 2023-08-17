from datetime import timedelta
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout

from .serializers import UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



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
            data['role'] = 'admin'  # Replace with the admin dashboard URL
        elif user.role == 'user':
            data['role'] = 'user'  # Replace with the user dashboard URL
        elif user.role == 'recruiter':
            data['role'] = 'recruiter'  # Replace with the recruiter dashboard URL

        data['username']=user.username

               
        response=Response(data, status=status.HTTP_200_OK)
        response.set_cookie('access_token',access_token,httponly=True)
        return response
class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        # Clear the token from the client's storage
        response = Response({'detail': 'Logout successful'})
        response.delete_cookie('access_token')  # Clear the access token cookie
        return response
        
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):

    user = request.user
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)