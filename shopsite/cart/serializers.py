from rest_framework import serializers
from .models import Cartitem,Wishlist
from product.models import Product
from product.serializers import ProductSerializer


class CartitemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cartitem
        fields=['id','product','quantity','added_at']
    
    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)

    # Check if product already in cart
        existing_item = Cartitem.objects.filter(product=product).first()

        if existing_item:
        # If product already exists, just increase quantity
          existing_item.quantity += quantity
          existing_item.save()
          return existing_item
        else:
        # If not found, create new cart item
            return Cartitem.objects.create(product=product, quantity=quantity)
        
class Wishlistserializer(serializers.ModelSerializer):
    class Meta:
        model=Wishlist
        fields='__all__'

