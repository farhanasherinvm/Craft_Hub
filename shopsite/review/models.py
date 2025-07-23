from django.db import models
from cart.models import Product
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator


class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    reply=models.TextField(blank=True,null=True)
    reply_at=models.DateTimeField(blank=True,null=True)