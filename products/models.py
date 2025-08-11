from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Currency(models.Model):
    """Modelo para moedas"""
    code = models.CharField(max_length=3, unique=True, verbose_name=_('products.currency_code'))
    name = models.CharField(max_length=50, verbose_name=_('products.currency_name'))
    symbol = models.CharField(max_length=5, verbose_name=_('products.currency_symbol'))
    
    class Meta:
        verbose_name = _('products.currency_verbose')
        verbose_name_plural = _('products.currency_verbose_plural')
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class ProductType(models.Model):
    """Modelo para tipos de produto"""
    name = models.CharField(max_length=100, verbose_name=_('common.name'))
    description = models.TextField(blank=True, verbose_name=_('common.description'))
    is_active = models.BooleanField(default=True, verbose_name=_('common.active'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('products.created_at'))
    
    class Meta:
        verbose_name = _('products.product_type_verbose')
        verbose_name_plural = _('products.product_type_verbose_plural')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Modelo para categorias de produto"""
    name = models.CharField(max_length=100, verbose_name=_('common.name'))
    description = models.TextField(blank=True, verbose_name=_('common.description'))
    is_active = models.BooleanField(default=True, verbose_name=_('common.active'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('products.created_at'))
    
    class Meta:
        verbose_name = _('products.category_verbose')
        verbose_name_plural = _('products.category_verbose_plural')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Scale(models.Model):
    """Modelo para escalas padronizadas"""
    name = models.CharField(max_length=50, unique=True, verbose_name=_('common.name'))
    description = models.TextField(blank=True, verbose_name=_('common.description'))
    is_active = models.BooleanField(default=True, verbose_name=_('common.active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('products.created_at'))
    
    class Meta:
        verbose_name = _('products.scale_verbose')
        verbose_name_plural = _('products.scale_verbose_plural')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Modelo para produtos"""
    DIMENSION_UNITS = [
        ('mm', _('products.millimeters')),
        ('cm', _('products.centimeters')),
        ('in', _('products.inches')),
    ]
    
    WEIGHT_UNITS = [
        ('g', _('products.grams')),
        ('kg', _('products.kilograms')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('common.name'))
    description = models.TextField(blank=True, verbose_name=_('common.description'))
    
    # Relacionamentos
    company = models.ForeignKey(
        'core.Company', 
        on_delete=models.CASCADE, 
        verbose_name=_('products.company')
    )
    product_type = models.ForeignKey(
        ProductType, 
        on_delete=models.CASCADE, 
        verbose_name=_('products.product_type')
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('products.category')
    )
    
    # Preços e moeda
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('products.cost_price')
    )
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('products.sale_price')
    )
    currency = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE, 
        verbose_name=_('products.currency')
    )
    
    # Escala
    scale = models.ForeignKey(
        Scale, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('products.scale')
    )
    
    # Dimensões
    dimensions_x = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('products.dimensions_x')
    )
    dimensions_y = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('products.dimensions_y')
    )
    dimensions_z = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('products.dimensions_z')
    )
    dimension_unit = models.CharField(
        max_length=2, 
        choices=DIMENSION_UNITS, 
        default='cm', 
        verbose_name=_('products.dimension_unit')
    )
    
    # Peso
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('products.weight')
    )
    weight_unit = models.CharField(
        max_length=2, 
        choices=WEIGHT_UNITS, 
        default='g', 
        verbose_name=_('products.weight_unit')
    )
    
    # Tempo de impressão
    print_time_estimate = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name=_('products.print_time_estimate')
    )
    
    # Estoque
    stock_quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name=_('products.stock_quantity')
    )
    
    # Controle
    is_active = models.BooleanField(default=True, verbose_name=_('common.active'))
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name=_('products.created_by')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('products.created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('products.updated_at'))
    
    class Meta:
        verbose_name = _('products.product_verbose')
        verbose_name_plural = _('products.product_verbose_plural')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_dimensions_display(self):
        """Retorna as dimensões formatadas"""
        if self.dimensions_x and self.dimensions_y and self.dimensions_z:
            return f"{self.dimensions_x} x {self.dimensions_y} x {self.dimensions_z} {self.get_dimension_unit_display()}"
        return ""
    
    def get_weight_display(self):
        """Retorna o peso formatado"""
        if self.weight:
            return f"{self.weight} {self.get_weight_unit_display()}"
        return ""


class ProductImage(models.Model):
    """Modelo para imagens do produto"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name=_('products.product_verbose')
    )
    image = models.ImageField(
        upload_to='products/images/', 
        verbose_name=_('products.images')
    )
    is_primary = models.BooleanField(
        default=False, 
        verbose_name=_('products.primary_image')
    )
    order_index = models.PositiveIntegerField(
        default=0, 
        verbose_name=_('products.order')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('products.created_at'))
    
    class Meta:
        verbose_name = _('products.product_image_verbose')
        verbose_name_plural = _('products.product_image_verbose_plural')
        ordering = ['order_index', 'created_at']
    
    def __str__(self):
        return f"Imagem de {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Se esta imagem for marcada como principal, desmarcar as outras
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs) 