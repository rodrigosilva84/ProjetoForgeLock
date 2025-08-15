#!/usr/bin/env python3
"""
Script para restaurar as imagens dos produtos
"""
import json
import os
import django
import shutil
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from products.models import ProductImage, Product

def restaurar_imagens():
    """Restaura as imagens dos produtos"""
    
    backup_file = 'backup_completo_20250814_234736.json'
    
    if not os.path.exists(backup_file):
        print(f"❌ Arquivo de backup não encontrado: {backup_file}")
        return False
    
    try:
        print("📖 Carregando backup...")
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        print("🖼️ Restaurando imagens dos produtos...")
        
        # Verificar se há imagens no backup
        if 'products_productimage' not in backup_data:
            print("❌ Tabela de imagens não encontrada no backup")
            return False
        
        images_data = backup_data['products_productimage']
        print(f"📸 Encontradas {len(images_data)} imagens no backup")
        
        restored_count = 0
        
        for image_record in images_data:
            try:
                # Buscar produto
                product_id = image_record.get('product_id')
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    print(f"⚠️ Produto ID {product_id} não encontrado, pulando imagem")
                    continue
                
                # Verificar se a imagem já existe
                existing_image = ProductImage.objects.filter(
                    product=product,
                    order_index=image_record.get('order_index', 0)
                ).first()
                
                if existing_image:
                    print(f"🔄 Imagem já existe para produto {product.name}")
                    continue
                
                # Criar nova imagem
                image = ProductImage.objects.create(
                    product=product,
                    order_index=image_record.get('order_index', 0),
                    is_primary=image_record.get('is_primary', False),
                    image=image_record.get('image', ''),
                )
                
                print(f"✅ Imagem criada para produto: {product.name}")
                restored_count += 1
                
            except Exception as e:
                print(f"❌ Erro ao restaurar imagem: {e}")
                continue
        
        print(f"\n🎉 Imagens restauradas: {restored_count}")
        
        # Verificar se há arquivos de imagem na pasta media
        media_dir = Path('media')
        if media_dir.exists():
            print(f"\n📁 Verificando pasta media: {media_dir}")
            product_images_dir = media_dir / 'product_images'
            if product_images_dir.exists():
                print(f"📸 Pasta de imagens encontrada: {product_images_dir}")
                image_files = list(product_images_dir.glob('*'))
                print(f"🖼️ Arquivos de imagem encontrados: {len(image_files)}")
                
                # Copiar imagens para o container se necessário
                print("🔄 As imagens devem estar disponíveis no container")
            else:
                print("⚠️ Pasta de imagens não encontrada")
        else:
            print("⚠️ Pasta media não encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao restaurar imagens: {e}")
        return False

def verificar_imagens_produtos():
    """Verifica as imagens dos produtos no banco"""
    
    print("\n🔍 VERIFICANDO IMAGENS DOS PRODUTOS NO BANCO")
    print("=" * 50)
    
    produtos = Product.objects.all()
    
    for produto in produtos:
        print(f"\n📦 Produto: {produto.name}")
        imagens = ProductImage.objects.filter(product=produto)
        
        if imagens:
            for img in imagens:
                print(f"  🖼️ Imagem: {img.image} (Principal: {img.is_primary})")
        else:
            print("  ⚠️ Nenhuma imagem encontrada")
    
    return True

if __name__ == '__main__':
    print("🚀 RESTAURANDO IMAGENS DOS PRODUTOS")
    print("=" * 50)
    
    success = restaurar_imagens()
    
    if success:
        print("\n✅ Restauração de imagens concluída!")
        verificar_imagens_produtos()
        print("\n🌐 Teste o site agora: http://127.0.0.1:8000/")
    else:
        print("\n❌ Restauração de imagens falhou!")
