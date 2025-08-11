from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Currency, ProductType, Category, Product, ProductImage


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'symbol']
    search_fields = ['code', 'name']
    ordering = ['code']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary', 'order_index']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'product_type', 'category', 'cost_price', 
        'sale_price', 'currency', 'stock_quantity', 'is_active', 
        'created_by', 'created_at'
    ]
    list_filter = [
        'product_type', 'category', 'currency', 'is_active', 
        'created_at', 'dimension_unit', 'weight_unit'
    ]
    search_fields = ['name', 'description', 'scale']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        (_('products.admin.basic_info'), {
            'fields': ('name', 'description', 'product_type', 'category')
        }),
        (_('products.admin.prices'), {
            'fields': ('cost_price', 'sale_price', 'currency')
        }),
        (_('products.admin.specifications'), {
            'fields': ('scale', 'dimensions_x', 'dimensions_y', 'dimensions_z', 'dimension_unit')
        }),
        (_('products.admin.weight_and_time'), {
            'fields': ('weight', 'weight_unit', 'print_time_estimate')
        }),
        (_('products.admin.stock'), {
            'fields': ('stock_quantity',)
        }),
        (_('products.admin.control'), {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é uma criação
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_primary', 'order_index', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']
    ordering = ['product', 'order_index']
