from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError



class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    


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
    product_type = models.CharField(max_length=20,)
    fabric = models.CharField(max_length=50, null=True,blank=True)
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

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    saved_for_later = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.email}"


# CartItem with stock validation
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def clean(self):
        if self.quantity > self.product.current_stock:
            raise ValidationError(f"Only {self.product.current_stock} items left in stock for {self.product.name}.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() to validate stock
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.quantity * self.product.wholesale_price


# Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} → {self.product.name}"