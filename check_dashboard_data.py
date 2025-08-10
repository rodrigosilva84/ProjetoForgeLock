#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from customers.models import Customer
from products.models import Product
from core.models import Company, User

# Verificar dados gerais
print("=== DADOS GERAIS ===")
print(f"Total de Clientes: {Customer.objects.count()}")
print(f"Total de Produtos: {Product.objects.count()}")
print(f"Total de Empresas: {Company.objects.count()}")

# Verificar dados por empresa
print("\n=== DADOS POR EMPRESA ===")
for company in Company.objects.all():
    print(f"\nEmpresa: {company.name}")
    customers = Customer.objects.filter(company=company)
    products = Product.objects.filter(company=company)
    users = User.objects.filter(companies=company)
    
    print(f"  - Clientes: {customers.count()}")
    print(f"  - Produtos: {products.count()}")
    print(f"  - Usuários: {users.count()}")
    
    if customers.exists():
        print("  - Clientes encontrados:")
        for customer in customers:
            print(f"    * {customer.name} ({customer.email})")
    
    if products.exists():
        print("  - Produtos encontrados:")
        for product in products:
            print(f"    * {product.name}")

# Verificar usuário tech_admin
print("\n=== USUÁRIO TECH_ADMIN ===")
try:
    tech_admin = User.objects.get(username='tech_admin')
    primary_company = tech_admin.get_primary_company()
    print(f"Usuário: {tech_admin.username}")
    print(f"Empresa principal: {primary_company.name if primary_company else 'Nenhuma'}")
    
    if primary_company:
        customers_count = Customer.objects.filter(company=primary_company).count()
        products_count = Product.objects.filter(company=primary_company).count()
        print(f"Clientes da empresa: {customers_count}")
        print(f"Produtos da empresa: {products_count}")
        
except User.DoesNotExist:
    print("Usuário tech_admin não encontrado")
