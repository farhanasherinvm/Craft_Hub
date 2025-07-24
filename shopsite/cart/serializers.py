from rest_framework import serializers
from .models import Cartitem,Wishlist
from product.models import Product
from product.serializers import ProductSerializer


class CartitemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cartitem
        fields=['id','product','quantity','added_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)  # default to 1 if not provided

        existing_item = Cartitem.objects.filter(user=user, product=product).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            return existing_item
        else:
            return Cartitem.objects.create(user=user, product=product, quantity=quantity)
class Wishlistserializer(serializers.ModelSerializer):
    class Meta:
        model=Wishlist
        fields='__all__'
        read_only_fields=['user']

