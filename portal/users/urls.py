from django.urls import path,include
from .views import UserRegistrationView, UserLoginView, user_profile
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('user-profile/', user_profile, name='user_profile'),

]
