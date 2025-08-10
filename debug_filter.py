#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from products.models import Product
from core.models import Company

# Simular a lógica da view
def test_filter_logic():
    print("=== DEBUG FILTRO DE STATUS ===")
    
    # Buscar empresa
    company = Company.objects.get(name='Pato Donald')
    print(f"Empresa: {company.name}")
    
    # Produtos base
    products = Product.objects.filter(company=company)
    print(f"Produtos base: {products.count()}")
    
    # Testar filtro 'active'
    status = 'active'
    print(f"\nTestando filtro: status = '{status}'")
    
    if status == 'active':
        filtered_products = products.filter(is_active=True)
        print(f"Produtos filtrados (ativo): {filtered_products.count()}")
        for product in filtered_products:
            print(f"  - {product.name} (ativo: {product.is_active})")
    
    # Testar filtro 'inactive'
    status = 'inactive'
    print(f"\nTestando filtro: status = '{status}'")
    
    if status == 'inactive':
        filtered_products = products.filter(is_active=False)
        print(f"Produtos filtrados (inativo): {filtered_products.count()}")
        for product in filtered_products:
            print(f"  - {product.name} (ativo: {product.is_active})")
    
    # Testar filtro vazio
    status = ''
    print(f"\nTestando filtro: status = '{status}' (vazio)")
    
    if status == 'active':
        filtered_products = products.filter(is_active=True)
    elif status == 'inactive':
        filtered_products = products.filter(is_active=False)
    else:
        filtered_products = products  # Mostra todos
    
    print(f"Produtos filtrados (vazio): {filtered_products.count()}")
    for product in filtered_products:
        print(f"  - {product.name} (ativo: {product.is_active})")

if __name__ == '__main__':
    test_filter_logic()
