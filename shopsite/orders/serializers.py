from rest_framework import serializers
from .models import Order, OrderItem, Address
from product.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_purchase']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    address_id = serializers.IntegerField(write_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address_id', 'total_price', 'status', 'ordered_at', 'items']
        read_only_fields = ['id', 'ordered_at', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        address_id = validated_data.pop('address_id')
        user = self.context['request'].user

        # Validate address
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError("Invalid address or does not belong to the user.")

        # Create the Order
        order = Order.objects.create(user=user, address=address, **validated_data)

        # Create each order item
        for item_data in items_data:
            product = item_data.get('product')
            if not product:
                raise serializers.ValidationError("Product must be provided for each item.")
            
            quantity = item_data.get('quantity', 1)
            price = product.wholesale_price or product.cost_price or 0.0

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=price
            )

        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
