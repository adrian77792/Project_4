from django.contrib import admin
from .models import Product, Category, Brand, ProductImage, ProductVariant
 
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
 
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'available', 'category')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'sku')
    list_filter = ('available', 'category', 'brand')
    inlines = [ProductImageInline, ProductVariantInline]
 
admin.site.register(Category)
admin.site.register(Brand)

