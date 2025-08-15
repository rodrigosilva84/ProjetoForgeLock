#!/usr/bin/env python3
"""
Script para restaurar apenas os produtos após a criação da tabela Scale
"""
import json
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from products.models import Product, Scale, Category, ProductType, Currency
from core.models import Company, User

def restaurar_produtos():
    """Restaura apenas os produtos do backup"""
    
    backup_file = 'backup_completo_20250814_234736.json'
    
    if not os.path.exists(backup_file):
        print(f"❌ Arquivo de backup não encontrado: {backup_file}")
        return False
    
    try:
        print("📖 Carregando backup...")
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        print("🔄 Restaurando produtos...")
        
        # Restaurar produtos
        if 'products_product' in backup_data:
            products_data = backup_data['products_product']
            print(f"📦 Encontrados {len(products_data)} produtos no backup")
            
            restored_count = 0
            
            for product_record in products_data:
                try:
                    # Buscar empresa pelo nome
                    company_name = product_record.get('company_name', '')
                    if company_name:
                        try:
                            company = Company.objects.get(name=company_name)
                        except Company.DoesNotExist:
                            print(f"⚠️ Empresa '{company_name}' não encontrada, pulando produto")
                            continue
                    else:
                        # Usar empresa padrão se não houver nome
                        company = Company.objects.first()
                    
                    # Buscar categoria - SEMPRE usar uma válida
                    category_name = product_record.get('category_name', '')
                    category = None
                    if category_name:
                        try:
                            category = Category.objects.get(name=category_name)
                        except Category.DoesNotExist:
                            print(f"⚠️ Categoria '{category_name}' não encontrada")
                    
                    # Se não encontrou categoria, usar a primeira disponível
                    if not category:
                        category = Category.objects.first()
                        if not category:
                            print("❌ Nenhuma categoria encontrada no banco!")
                            return False
                        print(f"⚠️ Usando categoria padrão: {category.name}")
                    
                    # Buscar tipo de produto - SEMPRE usar um válido
                    product_type_name = product_record.get('product_type_name', '')
                    product_type = None
                    if product_type_name:
                        try:
                            product_type = ProductType.objects.get(name=product_type_name)
                        except ProductType.DoesNotExist:
                            print(f"⚠️ Tipo de produto '{product_type_name}' não encontrado")
                    
                    # Se não encontrou tipo, usar o primeiro disponível
                    if not product_type:
                        product_type = ProductType.objects.first()
                        if not product_type:
                            print("❌ Nenhum tipo de produto encontrado no banco!")
                            return False
                        print(f"⚠️ Usando tipo padrão: {product_type.name}")
                    
                    # Buscar escala - SEMPRE usar uma válida
                    scale_name = product_record.get('scale_name', '')
                    scale = None
                    if scale_name:
                        try:
                            scale = Scale.objects.get(name=scale_name)
                        except Scale.DoesNotExist:
                            print(f"⚠️ Escala '{scale_name}' não encontrada")
                    
                    # Se não encontrou escala, usar a primeira disponível
                    if not scale:
                        scale = Scale.objects.first()
                        if not scale:
                            print("❌ Nenhuma escala encontrada no banco!")
                            return False
                        print(f"⚠️ Usando escala padrão: {scale.name}")
                    
                    # Buscar moeda
                    currency_code = product_record.get('currency_code', 'BRL')
                    try:
                        currency = Currency.objects.get(code=currency_code)
                    except Currency.DoesNotExist:
                        currency = Currency.objects.first()
                    
                    # Buscar usuário criador - SEMPRE usar um usuário válido
                    created_by_username = product_record.get('created_by_username', '')
                    created_by = None
                    
                    # Tentar encontrar o usuário pelo username
                    if created_by_username:
                        try:
                            created_by = User.objects.get(username=created_by_username)
                        except User.DoesNotExist:
                            pass
                    
                    # Se não encontrou, usar o primeiro usuário disponível
                    if not created_by:
                        created_by = User.objects.first()
                        if not created_by:
                            print("❌ Nenhum usuário encontrado no banco!")
                            return False
                        print(f"⚠️ Usando usuário padrão: {created_by.username}")
                    
                    # Criar produto
                    product, created = Product.objects.update_or_create(
                        id=product_record.get('id'),
                        defaults={
                            'name': product_record.get('name', ''),
                            'description': product_record.get('description', ''),
                            'company': company,
                            'category': category,
                            'product_type': product_type,
                            'scale': scale,
                            'currency': currency,
                            'cost_price': product_record.get('cost_price'),
                            'sale_price': product_record.get('sale_price'),
                            'stock_quantity': product_record.get('stock_quantity', 0),
                            'dimensions_x': product_record.get('dimensions_x'),
                            'dimensions_y': product_record.get('dimensions_y'),
                            'dimensions_z': product_record.get('dimensions_z'),
                            'dimension_unit': product_record.get('dimension_unit', 'cm'),
                            'weight': product_record.get('weight'),
                            'weight_unit': product_record.get('weight_unit', 'g'),
                            'print_time_estimate': product_record.get('print_time_estimate'),
                            'is_active': product_record.get('is_active', True),
                            'created_by': created_by,
                        }
                    )
                    
                    if created:
                        print(f"✅ Produto criado: {product.name} (Empresa: {company.name})")
                        restored_count += 1
                    else:
                        print(f"🔄 Produto atualizado: {product.name} (Empresa: {company.name})")
                        restored_count += 1
                        
                except Exception as e:
                    print(f"❌ Erro ao restaurar produto: {e}")
                    continue
            
            print(f"\n🎉 Produtos restaurados: {restored_count}")
            return True
            
        else:
            print("❌ Tabela de produtos não encontrada no backup")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao restaurar produtos: {e}")
        return False

if __name__ == '__main__':
    print("🚀 RESTAURANDO PRODUTOS DO BACKUP")
    print("=" * 50)
    
    success = restaurar_produtos()
    
    if success:
        print("\n✅ Restauração de produtos concluída!")
    else:
        print("\n❌ Restauração de produtos falhou!")
