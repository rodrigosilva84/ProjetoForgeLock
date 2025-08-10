#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import User, UserCompany, Company
from customers.models import Customer
from products.models import Product

# Verificar usuário tech_admin
print("=== VERIFICAÇÃO DO TECH_ADMIN ===")
try:
    tech_admin = User.objects.get(username='tech_admin')
    print(f"Usuário: {tech_admin.username}")
    print(f"Email: {tech_admin.email}")
    
    # Verificar empresas associadas
    user_companies = UserCompany.objects.filter(user=tech_admin)
    print(f"\nEmpresas associadas: {user_companies.count()}")
    
    for uc in user_companies:
        print(f"  - {uc.company.name} (role: {uc.role}, ativo: {uc.is_active})")
        
        # Verificar dados da empresa
        customers = Customer.objects.filter(company=uc.company)
        products = Product.objects.filter(company=uc.company)
        print(f"    * Clientes: {customers.count()}")
        print(f"    * Produtos: {products.count()}")
        
        if customers.exists():
            print("    * Clientes:")
            for customer in customers:
                print(f"      - {customer.name} ({customer.email})")
        
        if products.exists():
            print("    * Produtos:")
            for product in products:
                print(f"      - {product.name}")
    
    # Verificar empresa principal
    primary_company = tech_admin.get_primary_company()
    print(f"\nEmpresa principal: {primary_company.name if primary_company else 'Nenhuma'}")
    
    if primary_company:
        customers_count = Customer.objects.filter(company=primary_company).count()
        products_count = Product.objects.filter(company=primary_company).count()
        print(f"Clientes da empresa principal: {customers_count}")
        print(f"Produtos da empresa principal: {products_count}")
        
except User.DoesNotExist:
    print("Usuário tech_admin não encontrado")

print("\n=== TODAS AS EMPRESAS ===")
for company in Company.objects.all():
    print(f"\nEmpresa: {company.name}")
    customers = Customer.objects.filter(company=company)
    products = Product.objects.filter(company=company)
    users = User.objects.filter(companies=company)
    
    print(f"  - Clientes: {customers.count()}")
    print(f"  - Produtos: {products.count()}")
    print(f"  - Usuários: {users.count()}")
    
    if customers.exists():
        print("  - Clientes:")
        for customer in customers:
            print(f"    * {customer.name} ({customer.email})")
    
    if products.exists():
        print("  - Produtos:")
        for product in products:
            print(f"    * {product.name}")
