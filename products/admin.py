from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import Product, Category, Brand, ProductImage


class CleanForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            value = str(value).strip()
        return super().clean(value, row=row, *args, **kwargs)


class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=CleanForeignKeyWidget(Category, 'name')
    )
    brand = fields.Field(
        column_name='brand',
        attribute='brand',
        widget=CleanForeignKeyWidget(Brand, 'name')
    )

    class Meta:
        model = Product
        skip_unchanged = True
        report_skipped = False


class ProductImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductImage
    extra = 1




@admin.register(Product)
class ProductAdmin(SortableAdminMixin, ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'sku', 'price', 'available', 'category', 'order')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'sku')
    list_filter = ('available', 'category', 'brand')
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'order')