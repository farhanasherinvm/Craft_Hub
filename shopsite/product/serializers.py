from rest_framework import serializers
from .models import Product, ProductImage,ProductCategory

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
