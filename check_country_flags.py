#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Country

def check_country_flags():
    """Verifica os dados dos países"""
    countries = Country.objects.all()
    
    print("=== VERIFICAÇÃO DE PAÍSES ===")
    for country in countries:
        print(f"País: {country.name} (Código: {country.code})")
        print(f"  - Flag: {country.flag}")
        print(f"  - Ativo: {country.is_active}")
        
        # Verificar se o arquivo existe
        if country.flag:
            flag_path = f"static/images/flags/{country.flag}.svg"
            if os.path.exists(flag_path):
                print(f"  - ✅ Arquivo existe: {flag_path}")
            else:
                print(f"  - ❌ Arquivo não existe: {flag_path}")
        else:
            print(f"  - ⚠️  Sem bandeira definida")
        print()

if __name__ == "__main__":
    check_country_flags()
