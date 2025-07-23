from django.shortcuts import render
from rest_framework import viewsets,permissions,generics,status
from .models import Cartitem,Wishlist
from .serializers import CartitemSerializer,Wishlistserializer
from rest_framework.response import Response



# List cart items
class CartListview(generics.ListAPIView):
    queryset=Cartitem.objects.all()
    serializer_class=CartitemSerializer
    permission_classes=[permissions.IsAuthenticated]     

# create items to cart
class Cartcreateview(generics.CreateAPIView):
    serializer_class=CartitemSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

# Update Cart items 
class Cartupdateview(generics.UpdateAPIView):
    serializer_class=CartitemSerializer
    permission_classes=[permissions.IsAuthenticated]    

    def get_queryset(self,):
        return Cartitem.objects.filter(user=self.request.user)                  #------- After add authentication add user inside serializer.save

    

# Delete cart items
class Cartdeleteview(generics.DestroyAPIView):
    serializer_class=CartitemSerializer
    permission_classes=[permissions.IsAuthenticated]     

    def get_queryset(self):
        return Cartitem.objects.filter(user=self.request.user)                 
    

class Wishlistview(generics.ListCreateAPIView):
    queryset=Wishlist.objects.all()
    serializer_class=Wishlistserializer
    permission_classes=[permissions.IsAuthenticated]     
    
    def get_queryset(self):
        # Only show wishlist items for the logged-in user
        return Wishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)                                 

class Wishlistdeleteview(generics.DestroyAPIView):
    serializer_class=Wishlistserializer
    permission_classes=[permissions.IsAuthenticated]     

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)                  
    