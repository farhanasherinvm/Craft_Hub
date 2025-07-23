from django.contrib import admin
from users.models import CustomUser
from cart.models import Cartitem,Wishlist
from review.models import Review
from product.models import Product

class CustomUserAdmin(CustomUser):
    model = CustomUser

    list_display = ('email', 'phone_number', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Other Info', {'fields': ('role', 'otp')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'role')}
        ),
    )

    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser)
admin.site.register(Cartitem)
admin.site.register(Wishlist)
admin.site.register(Review)



