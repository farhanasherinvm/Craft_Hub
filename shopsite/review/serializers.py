from rest_framework import serializers
from .models import Review


class Reviewserializer(serializers.ModelSerializer):
    reviewer_name=serializers.CharField(source='user.first_name',read_only=True)

    class Meta:
        model=Review
        fields=['id', 'user', 'reviewer_name', 'rating', 'product', 'comment', 'created_at', 'reply', 'reply_at']
        read_only_fields=['id','user','created_at','reply','reply_at','reviewer_name',]

class Replyserializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['reply','reply_at']
        read_only_fields=['reply_at']