#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Country

def fix_country_flags():
    """Corrige os dados das bandeiras dos países"""
    countries = Country.objects.all()
    
    print("=== CORRIGINDO BANDEIRAS DOS PAÍSES ===")
    for country in countries:
        print(f"País: {country.name} (Código: {country.code})")
        
        # Verificar se o campo flag tem extensão .svg
        if country.flag and country.flag.endswith('.svg'):
            # Remover a extensão .svg
            new_flag = country.flag.replace('.svg', '')
            country.flag = new_flag
            country.save()
            print(f"  - ✅ Corrigido: {country.flag} -> {new_flag}")
        elif country.flag:
            print(f"  - ℹ️  Já correto: {country.flag}")
        else:
            print(f"  - ⚠️  Sem bandeira definida")
        print()

if __name__ == "__main__":
    fix_country_flags()
