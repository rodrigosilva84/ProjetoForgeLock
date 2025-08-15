#!/usr/bin/env python3
"""
Script para verificar produtos e empresas no banco PostgreSQL
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Company, UserCompany
from products.models import Product, Scale, Category, ProductType
from core.models import User

def verificar_dados():
    """Verifica os dados no banco PostgreSQL"""
    
    print("🔍 VERIFICANDO DADOS NO BANCO POSTGRESQL")
    print("=" * 50)
    
    # Verificar Empresas
    print("\n🏢 EMPRESAS:")
    companies = Company.objects.all()
    for company in companies:
        print(f"  - ID: {company.id} | Nome: {company.name} | CNPJ: {company.cnpj}")
    
    # Verificar Usuários e suas Empresas
    print("\n👤 USUÁRIOS E EMPRESAS:")
    user_companies = UserCompany.objects.all()
    for uc in user_companies:
        print(f"  - Usuário: {uc.user.username} | Empresa: {uc.company.name} | Role: {uc.role}")
    
    # Verificar Produtos
    print("\n📦 PRODUTOS:")
    products = Product.objects.all()
    if products:
        for product in products:
            company_name = product.company.name if product.company else "Sem empresa"
            print(f"  - ID: {product.id} | Nome: {product.name} | Empresa: {company_name} | Ativo: {product.is_active}")
    else:
        print("  ⚠️ Nenhum produto encontrado!")
    
    # Verificar Escalas
    print("\n📏 ESCALAS:")
    scales = Scale.objects.all()
    for scale in scales:
        print(f"  - ID: {scale.id} | Nome: {scale.name} | Ativo: {scale.is_active}")
    
    # Verificar Categorias
    print("\n🏷️ CATEGORIAS:")
    categories = Category.objects.all()
    for category in categories:
        print(f"  - ID: {category.id} | Nome: {category.name} | Ativo: {category.is_active}")
    
    # Verificar Tipos de Produto
    print("\n🔧 TIPOS DE PRODUTO:")
    product_types = ProductType.objects.all()
    for pt in product_types:
        print(f"  - ID: {pt.id} | Nome: {pt.name} | Ativo: {pt.is_active}")
    
    # Verificar Usuário tech_admin
    print("\n🔐 USUÁRIO TECH_ADMIN:")
    try:
        tech_admin = User.objects.get(username='tech_admin')
        print(f"  - Username: {tech_admin.username}")
        print(f"  - Email: {tech_admin.email}")
        print(f"  - Ativo: {tech_admin.is_active}")
        
        # Verificar empresa do tech_admin
        tech_admin_companies = UserCompany.objects.filter(user=tech_admin)
        if tech_admin_companies:
            for uc in tech_admin_companies:
                print(f"  - Empresa: {uc.company.name} | Role: {uc.role}")
        else:
            print("  ⚠️ tech_admin não está associado a nenhuma empresa!")
            
    except User.DoesNotExist:
        print("  ❌ Usuário tech_admin não encontrado!")

if __name__ == '__main__':
    verificar_dados()
