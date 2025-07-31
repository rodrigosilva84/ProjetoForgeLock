#!/usr/bin/env python
"""
Script para testar formatação de números de telefone
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Country, User
from core.services import VerificationService

def test_phone_formats():
    """Testa diferentes formatos de número de telefone"""
    print("Teste de Formatação de Números de Telefone")
    print("=" * 50)
    
    # Buscar Brasil
    try:
        brazil = Country.objects.get(code='BR')
        print(f"País: {brazil.name} (DDI: {brazil.ddi})")
    except Country.DoesNotExist:
        print("ERROR: Brasil não encontrado no banco!")
        return
    
    # Diferentes formatos para testar
    test_numbers = [
        "(11) 99999-9999",  # Formato com parênteses e hífen
        "11999999999",       # Apenas números
        "11 99999 9999",     # Com espaços
        "+55 11 99999-9999", # Com + e DDI
        "5511999999999",      # Com DDI sem +
        "99999-9999",         # Sem DDI
        "999999999",          # Apenas número local
    ]
    
    verification_service = VerificationService()
    
    for number in test_numbers:
        print(f"\nTestando: '{number}'")
        try:
            formatted = verification_service._format_phone_number(number, brazil.ddi)
            print(f"  Resultado: {formatted}")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")

if __name__ == "__main__":
    test_phone_formats() 