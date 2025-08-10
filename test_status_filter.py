#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from products.models import Product
from core.models import Company

# Testar filtro de status
print("=== TESTE DO FILTRO DE STATUS ===")

# Buscar empresa Pato Donald
company = Company.objects.get(name='Pato Donald')
print(f"Empresa: {company.name}")

# Produtos sem filtro
all_products = Product.objects.filter(company=company)
print(f"\nTotal de produtos: {all_products.count()}")

# Produtos ativos
active_products = Product.objects.filter(company=company, is_active=True)
print(f"Produtos ativos: {active_products.count()}")
for product in active_products:
    print(f"  - {product.name} (ativo: {product.is_active})")

# Produtos inativos
inactive_products = Product.objects.filter(company=company, is_active=False)
print(f"\nProdutos inativos: {inactive_products.count()}")
for product in inactive_products:
    print(f"  - {product.name} (ativo: {product.is_active})")

# Simular filtro 'active'
print(f"\n=== SIMULANDO FILTRO 'active' ===")
status = 'active'
if status == 'active':
    filtered_products = Product.objects.filter(company=company, is_active=True)
    print(f"Produtos filtrados (ativo): {filtered_products.count()}")
    for product in filtered_products:
        print(f"  - {product.name} (ativo: {product.is_active})")

# Simular filtro 'inactive'
print(f"\n=== SIMULANDO FILTRO 'inactive' ===")
status = 'inactive'
if status == 'inactive':
    filtered_products = Product.objects.filter(company=company, is_active=False)
    print(f"Produtos filtrados (inativo): {filtered_products.count()}")
    for product in filtered_products:
        print(f"  - {product.name} (ativo: {product.is_active})")
