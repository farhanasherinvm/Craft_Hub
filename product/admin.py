from django.contrib import admin
from .models import Product, ProductImage

# Inline to handle multiple image uploads in the same page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty image fields to show

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'fabric', 'color', 'size', 'current_stock', 'is_draft', 'allow_customization')
    list_filter = ('product_type', 'fabric', 'color', 'size', 'is_draft', 'allow_customization')
    search_fields = ('name', 'product_code', 'sku')
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'product_type', 'fabric', 'color', 'size', 'product_code', 'stock_keeping_unit')
        }),
        ('Pricing & Inventory', {
            'fields': ('cost_price', 'wholesale_price', 'min_order_quantity', 'current_stock', 'allow_customization')
        }),
        ('Description', {
            'fields': ('description', 'is_draft')
        }),
    )
