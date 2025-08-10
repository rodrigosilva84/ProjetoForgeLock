from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Currency(models.Model):
    """Modelo para moedas"""
    code = models.CharField(max_length=3, unique=True, verbose_name=_('Código'))
    name = models.CharField(max_length=50, verbose_name=_('Nome'))
    symbol = models.CharField(max_length=5, verbose_name=_('Símbolo'))
    
    class Meta:
        verbose_name = _('Moeda')
        verbose_name_plural = _('Moedas')
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class ProductType(models.Model):
    """Modelo para tipos de produto"""
    name = models.CharField(max_length=100, verbose_name=_('Nome'))
    description = models.TextField(blank=True, verbose_name=_('Descrição'))
    
    class Meta:
        verbose_name = _('Tipo de Produto')
        verbose_name_plural = _('Tipos de Produto')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Modelo para categorias de produto"""
    name = models.CharField(max_length=100, verbose_name=_('Nome'))
    description = models.TextField(blank=True, verbose_name=_('Descrição'))
    
    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Modelo para produtos"""
    DIMENSION_UNITS = [
        ('mm', _('Milímetros')),
        ('cm', _('Centímetros')),
        ('in', _('Polegadas')),
    ]
    
    WEIGHT_UNITS = [
        ('g', _('Gramas')),
        ('kg', _('Quilogramas')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Nome'))
    description = models.TextField(blank=True, verbose_name=_('Descrição'))
    
    # Relacionamentos
    product_type = models.ForeignKey(
        ProductType, 
        on_delete=models.CASCADE, 
        verbose_name=_('Tipo de Produto')
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Categoria')
    )
    
    # Preços e moeda
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('Preço de Custo')
    )
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('Preço de Venda')
    )
    currency = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE, 
        verbose_name=_('Moeda')
    )
    
    # Escala
    scale = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name=_('Escala')
    )
    
    # Dimensões
    dimensions_x = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('Largura')
    )
    dimensions_y = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('Altura')
    )
    dimensions_z = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('Profundidade')
    )
    dimension_unit = models.CharField(
        max_length=2, 
        choices=DIMENSION_UNITS, 
        default='cm', 
        verbose_name=_('Unidade de Dimensão')
    )
    
    # Peso
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name=_('Peso')
    )
    weight_unit = models.CharField(
        max_length=2, 
        choices=WEIGHT_UNITS, 
        default='g', 
        verbose_name=_('Unidade de Peso')
    )
    
    # Tempo de impressão
    print_time_estimate = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name=_('Tempo de Impressão Estimado')
    )
    
    # Estoque
    stock_quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name=_('Quantidade em Estoque')
    )
    
    # Controle
    is_active = models.BooleanField(default=True, verbose_name=_('Ativo'))
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name=_('Criado por')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Atualizado em'))
    
    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
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
        verbose_name=_('Produto')
    )
    image = models.ImageField(
        upload_to='products/images/', 
        verbose_name=_('Imagem')
    )
    is_primary = models.BooleanField(
        default=False, 
        verbose_name=_('Imagem Principal')
    )
    order_index = models.PositiveIntegerField(
        default=0, 
        verbose_name=_('Ordem')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Criado em'))
    
    class Meta:
        verbose_name = _('Imagem do Produto')
        verbose_name_plural = _('Imagens do Produto')
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