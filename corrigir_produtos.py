#!/usr/bin/env python3
"""
Script para corrigir as associações dos produtos restaurados
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from products.models import Product, Scale, Category, ProductType
from core.models import Company, User

def corrigir_produtos():
    """Corrige as associações dos produtos"""
    
    print("🔧 CORRIGINDO ASSOCIAÇÕES DOS PRODUTOS")
    print("=" * 50)
    
    try:
        # Buscar empresas
        pato_donald = Company.objects.get(name='Pato Donald')
        rc_imports = Company.objects.get(name='RC Imports')
        
        # Buscar usuários
        pato_donald_user = User.objects.get(username='pato_donald')
        tech_admin = User.objects.get(username='tech_admin')
        
        # Buscar valores padrão
        categoria_padrao = Category.objects.get(name='Action Figures')
        tipo_padrao = ProductType.objects.get(name='Arquivo STL')
        escala_padrao = Scale.objects.get(name='1:1')
        
        print(f"🏢 Empresa Pato Donald: {pato_donald.name}")
        print(f"🏢 Empresa RC Imports: {rc_imports.name}")
        print(f"👤 Usuário Pato Donald: {pato_donald_user.username}")
        print(f"👤 Usuário Tech Admin: {tech_admin.username}")
        
        # Corrigir produtos
        produtos = Product.objects.all()
        print(f"\n📦 Encontrados {produtos.count()} produtos para corrigir")
        
        for produto in produtos:
            print(f"\n🔄 Corrigindo produto: {produto.name}")
            
            # Associar à empresa Pato Donald
            produto.company = pato_donald
            
            # Associar ao usuário pato_donald
            produto.created_by = pato_donald_user
            
            # Manter valores padrão para outros campos
            produto.category = categoria_padrao
            produto.product_type = tipo_padrao
            produto.scale = escala_padrao
            
            # Salvar alterações
            produto.save()
            
            print(f"✅ Produto corrigido: {produto.name}")
            print(f"   - Empresa: {produto.company.name}")
            print(f"   - Usuário: {produto.created_by.username}")
            print(f"   - Categoria: {produto.category.name}")
            print(f"   - Tipo: {produto.product_type.name}")
            print(f"   - Escala: {produto.scale.name}")
        
        print(f"\n🎉 Correção concluída! {produtos.count()} produtos corrigidos")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir produtos: {e}")
        return False

if __name__ == '__main__':
    success = corrigir_produtos()
    
    if success:
        print("\n✅ Produtos corrigidos com sucesso!")
        print("🌐 Teste o site agora: http://127.0.0.1:8000/")
    else:
        print("\n❌ Correção falhou!")
