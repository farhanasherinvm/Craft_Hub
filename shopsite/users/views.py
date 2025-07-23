from django.shortcuts import render
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import RegisterSerializer,PasswordResetRequestSerializer
from .models import PasswordResetOTP
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from notifications.utils import send_notification_email


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            subject = "Welcome to Our Wholesale Clothing Platform!"
            message = (
                f"Hello {user.first_name},\n\n"
                "Thank you for registering with us. We're excited to have you on board! "
                "Start exploring our products and enjoy exclusive offers."
                "\n\nBest regards,\nThe Team"
            )
            # Send the email to the user's registered email address
            send_notification_email(subject, message, [user.email])
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = str(random.randint(100000, 999999))

            # Save OTP to DB
            PasswordResetOTP.objects.create(email=email, otp=otp)

            # Send OTP via Email
            send_mail(
                subject='🔐 Password Reset OTP',
                message=f'Your OTP is: {otp}',
                from_email='your_email@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({'message': '✅ OTP sent successfully to email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
