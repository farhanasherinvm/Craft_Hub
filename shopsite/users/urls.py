from django.contrib import admin
from django.urls import path,include
from users import views
from rest_framework.routers import DefaultRouter
from .views import RegisterView,LogoutView,PasswordResetRequestView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

urlpatterns = [
        path('register/', views.RegisterView.as_view(), name='register'),
        path("logout/", views.LogoutView.as_view(), name="logout"),
        path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
 
        # JWT endpoints
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # access + refresh token
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # refresh access token
]
         
