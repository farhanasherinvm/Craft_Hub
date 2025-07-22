from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('saree', 'Saree'),
        ('shirt', 'Shirt'),
        ('dhoti', 'Dhoti'),
    ]

    FABRIC_CHOICES = [
        ('fabric_1', 'Fabric 1'),
        ('fabric_2', 'Fabric 2'),
        ('fabric_3', 'Fabric 3'),
        
    ]


    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    ]
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    fabric = models.CharField(max_length=50, choices=FABRIC_CHOICES)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    product_code = models.CharField(max_length=50, unique=True)
    stock_keeping_unit = models.CharField(max_length=50, unique=True)

    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_quantity = models.PositiveIntegerField(default=1)
    current_stock = models.PositiveIntegerField(default=0)
    allow_customization = models.BooleanField(default=False)

    description = models.TextField()
    is_draft = models.BooleanField(default=False)  # for Save as Draft

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"
