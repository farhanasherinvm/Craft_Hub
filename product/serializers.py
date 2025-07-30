from rest_framework import serializers
from .models import Product, ProductImage,ProductCategory
from .models import  Cart, CartItem, Wishlist

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), source='category', write_only=True
    )
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_id', 'name', 'product_type', 'fabric', 'color', 'size',
            'product_code', 'stock_keeping_unit', 'cost_price',
            'wholesale_price', 'min_order_quantity', 'current_stock',
            'allow_customization', 'description', 'is_draft', 'images'
        ]

# Cart Item Serializer with stock validation
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.wholesale_price

    def validate(self, data):
        product = data.get('product') or getattr(self.instance, 'product', None)
        quantity = data.get('quantity') or getattr(self.instance, 'quantity', None)

        if not product or not quantity:
            raise serializers.ValidationError("Product and quantity are required.")

        if quantity > product.current_stock:
            raise serializers.ValidationError({
                "quantity": f"Only {product.current_stock} item(s) available for {product.name}."
            })
        return data


# Cart Serializer (includes items)
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'saved_for_later']
        read_only_fields = ['user']


# Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_name', 'product_details', 'added_at']