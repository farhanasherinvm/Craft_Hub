from django.db import models

from users.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (('admin', 'Admin'), ('customer', 'Customer'))

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.first_name




class PasswordResetOTP(models.Model):
    email = models.EmailField(null=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.otp}"