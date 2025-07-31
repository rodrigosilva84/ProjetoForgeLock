#!/usr/bin/env python
"""
Script para testar o número específico do usuário
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Country
from core.services import VerificationService

def test_specific_number():
    """Testa o número específico do usuário"""
    print("Teste do Número Específico")
    print("=" * 50)
    
    # Buscar Brasil
    try:
        brazil = Country.objects.get(code='BR')
        print(f"País: {brazil.name} (DDI: {brazil.ddi})")
    except Country.DoesNotExist:
        print("ERROR: Brasil não encontrado no banco!")
        return
    
    # Número do usuário
    user_number = "17981690470"
    
    verification_service = VerificationService()
    
    print(f"\nTestando número: '{user_number}'")
    try:
        formatted = verification_service._format_phone_number(user_number, brazil.ddi)
        print(f"Resultado formatado: {formatted}")
        
        # Verificar se o formato está correto
        if formatted.startswith('+55') and len(formatted) == 13:
            print("✅ Formato correto!")
        else:
            print("❌ Formato incorreto!")
            
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")

if __name__ == "__main__":
    test_specific_number() 