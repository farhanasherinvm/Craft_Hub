from django.shortcuts import render
from.serializers import Reviewserializer,Replyserializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,permissions
from .models import Review
from rest_framework.exceptions import PermissionDenied 
from django.utils import timezone



class Reviewcreateview(generics.CreateAPIView):
    serializer_class=Reviewserializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class Reviewlist(generics.ListAPIView):
    serializer_class=Reviewserializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        product_id=self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)
class Replyreview(generics.UpdateAPIView):
    serializer_class=Replyserializer
    permission_classes=[IsAuthenticated]
    queryset=Review.objects.all()


    def perform_update(self, serializer):
        review_reply=self.get_object()
        user=self.request.user

        if not user.is_staff:
            raise PermissionDenied("only admins can reply to reviews")
        
        serializer.save(reply_at=timezone.now())




        
