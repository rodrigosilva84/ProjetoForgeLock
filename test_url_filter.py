#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from django.test import RequestFactory
from core.models import User
from products.views import product_list

def test_url_filter():
    print("=== TESTE URL FILTRO ===")
    
    factory = RequestFactory()
    user = User.objects.get(username='tech_admin')
    
    # Testar URL sem filtro
    print("\n1. Testando URL sem filtro:")
    request = factory.get('/products/')
    request.user = user
    response = product_list(request)
    print(f"Status: {response.status_code}")
    if hasattr(response, 'context_data'):
        print(f"Produtos: {len(response.context_data.get('page_obj', []))}")
        print(f"Status no contexto: {response.context_data.get('status')}")
    
    # Testar URL com filtro ativo
    print("\n2. Testando URL com filtro 'active':")
    request = factory.get('/products/?status=active')
    request.user = user
    response = product_list(request)
    print(f"Status: {response.status_code}")
    if hasattr(response, 'context_data'):
        print(f"Produtos: {len(response.context_data.get('page_obj', []))}")
        print(f"Status no contexto: {response.context_data.get('status')}")
    
    # Testar URL com filtro inativo
    print("\n3. Testando URL com filtro 'inactive':")
    request = factory.get('/products/?status=inactive')
    request.user = user
    response = product_list(request)
    print(f"Status: {response.status_code}")
    if hasattr(response, 'context_data'):
        print(f"Produtos: {len(response.context_data.get('page_obj', []))}")
        print(f"Status no contexto: {response.context_data.get('status')}")

if __name__ == '__main__':
    test_url_filter()
