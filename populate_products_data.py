#!/usr/bin/env python
"""
Script para popular dados iniciais de produtos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from products.models import Currency, ProductType, Category


def create_currencies():
    """Criar moedas iniciais"""
    currencies_data = [
        {'code': 'BRL', 'name': 'Real Brasileiro', 'symbol': 'R$'},
        {'code': 'USD', 'name': 'Dólar Americano', 'symbol': '$'},
        {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
    ]
    
    for data in currencies_data:
        currency, created = Currency.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"✅ Moeda criada: {currency}")
        else:
            print(f"ℹ️  Moeda já existe: {currency}")


def create_product_types():
    """Criar tipos de produto iniciais"""
    types_data = [
        {
            'name': 'STL',
            'description': 'Arquivo digital para impressão 3D'
        },
        {
            'name': 'Modelo Físico',
            'description': 'Produto já impresso/confecionado'
        },
        {
            'name': 'Serviço',
            'description': 'Impressão 3D, modelagem, etc.'
        },
    ]
    
    for data in types_data:
        product_type, created = ProductType.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✅ Tipo de produto criado: {product_type}")
        else:
            print(f"ℹ️  Tipo de produto já existe: {product_type}")


def create_categories():
    """Criar categorias iniciais"""
    categories_data = [
        {'name': 'Modelagem', 'description': 'Modelos 3D para impressão'},
        {'name': 'Action Figures', 'description': 'Figuras de ação'},
        {'name': 'Dioramas', 'description': 'Cenários e composições'},
        {'name': 'RPG', 'description': 'Itens para role-playing games'},
        {'name': 'Ímãs de Geladeira', 'description': 'Decoração'},
        {'name': 'Gospel', 'description': 'Itens religiosos'},
        {'name': 'Decoração', 'description': 'Outros itens decorativos'},
        {'name': 'Ferramentas', 'description': 'Utilitários'},
        {'name': 'Outros', 'description': 'Categoria genérica'},
    ]
    
    for data in categories_data:
        category, created = Category.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✅ Categoria criada: {category}")
        else:
            print(f"ℹ️  Categoria já existe: {category}")


def main():
    """Função principal"""
    print("🚀 Populando dados iniciais de produtos...")
    print()
    
    print("📊 Criando moedas...")
    create_currencies()
    print()
    
    print("🏷️  Criando tipos de produto...")
    create_product_types()
    print()
    
    print("📂 Criando categorias...")
    create_categories()
    print()
    
    print("✅ Dados iniciais criados com sucesso!")
    print()
    print("📋 Resumo:")
    print(f"- Moedas: {Currency.objects.count()}")
    print(f"- Tipos de Produto: {ProductType.objects.count()}")
    print(f"- Categorias: {Category.objects.count()}")


if __name__ == '__main__':
    main() 