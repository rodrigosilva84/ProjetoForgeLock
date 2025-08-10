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
