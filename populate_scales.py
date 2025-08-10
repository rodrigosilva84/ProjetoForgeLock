#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from products.models import Scale

def populate_scales():
    """Popular escalas padrão"""
    scales_data = [
        {'name': '1:1', 'description': 'Escala real (tamanho original)'},
        {'name': '1:4', 'description': 'Escala 1 para 4'},
        {'name': '1:6', 'description': 'Escala 1 para 6'},
        {'name': '1:8', 'description': 'Escala 1 para 8'},
        {'name': '1:10', 'description': 'Escala 1 para 10'},
        {'name': 'Outros', 'description': 'Outras escalas personalizadas'},
    ]
    
    created_count = 0
    for scale_data in scales_data:
        scale, created = Scale.objects.get_or_create(
            name=scale_data['name'],
            defaults={
                'description': scale_data['description'],
                'is_active': True
            }
        )
        if created:
            created_count += 1
            print(f"✅ Escala criada: {scale.name}")
        else:
            print(f"ℹ️  Escala já existe: {scale.name}")
    
    print(f"\n🎯 Total de escalas criadas: {created_count}")
    print(f"📊 Total de escalas no sistema: {Scale.objects.count()}")

if __name__ == '__main__':
    print("🚀 Populando escalas padrão...")
    populate_scales()
    print("✅ Concluído!")
