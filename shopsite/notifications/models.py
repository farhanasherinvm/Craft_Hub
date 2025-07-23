from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()




NOTIFICATION_TYPES = (
        ('ORDER_PLACED', 'Order Placed'),
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('PRODUCT_ADDED', 'New Product Added'),
        ('PROMOTION', 'Promotional Offer'),
)

NOTIFICATION_STATUSES = (
    ('SENT', 'Sent'),
    ('DELIVERED', 'Delivered'),
    ('READ', 'Read'),
    ('FAILED', 'Failed'),
)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUSES, default='SENT')
    created_at = models.DateTimeField(default=timezone.now)
    

   
    def __str__(self):
        return f"Notification #{self.id} - {self.title} ({self.notification_type})"

    class Meta:
        db_table = 'notifications'