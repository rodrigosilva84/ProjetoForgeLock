#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from django.test import RequestFactory
from django.template.loader import render_to_string
from core.models import User
from products.views import product_list

def test_template_render():
    print("=== TESTE RENDERIZAÇÃO TEMPLATE ===")
    
    factory = RequestFactory()
    user = User.objects.get(username='tech_admin')
    
    # Testar renderização com filtro ativo
    print("\n1. Testando renderização com filtro 'active':")
    request = factory.get('/products/?status=active')
    request.user = user
    response = product_list(request)
    
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"Status no contexto: {context.get('status')}")
        print(f"Produtos no contexto: {len(context.get('page_obj', []))}")
        
        # Verificar produtos
        for product in context.get('page_obj', []):
            print(f"  - {product.name} (ativo: {product.is_active})")
    
    # Testar renderização com filtro inativo
    print("\n2. Testando renderização com filtro 'inactive':")
    request = factory.get('/products/?status=inactive')
    request.user = user
    response = product_list(request)
    
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"Status no contexto: {context.get('status')}")
        print(f"Produtos no contexto: {len(context.get('page_obj', []))}")
        
        # Verificar produtos
        for product in context.get('page_obj', []):
            print(f"  - {product.name} (ativo: {product.is_active})")

if __name__ == '__main__':
    test_template_render()
