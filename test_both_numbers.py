#!/usr/bin/env python
"""
Script para testar ambos os números e comparar resultados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Country
from core.services import VerificationService

def test_both_numbers():
    """Testa ambos os números para comparar"""
    print("Teste Comparativo de Números")
    print("=" * 50)
    
    # Buscar Brasil
    try:
        brazil = Country.objects.get(code='BR')
        print(f"País: {brazil.name} (DDI: {brazil.ddi})")
    except Country.DoesNotExist:
        print("ERROR: Brasil não encontrado no banco!")
        return
    
    # Números para testar
    working_number = "17981839329"  # Funciona
    failing_number = "17981690470"  # Não funciona
    
    verification_service = VerificationService()
    
    print(f"\n{'='*20} NÚMERO QUE FUNCIONA {'='*20}")
    print(f"Testando: '{working_number}'")
    try:
        formatted_working = verification_service._format_phone_number(working_number, brazil.ddi)
        print(f"Formatado: {formatted_working}")
        
        # Simular envio
        print("Simulando envio...")
        # Aqui você pode adicionar teste real se quiser
        
    except Exception as e:
        print(f"ERROR: {e}")
    
    print(f"\n{'='*20} NÚMERO QUE NÃO FUNCIONA {'='*20}")
    print(f"Testando: '{failing_number}'")
    try:
        formatted_failing = verification_service._format_phone_number(failing_number, brazil.ddi)
        print(f"Formatado: {formatted_failing}")
        
        # Simular envio
        print("Simulando envio...")
        # Aqui você pode adicionar teste real se quiser
        
    except Exception as e:
        print(f"ERROR: {e}")
    
    print(f"\n{'='*20} COMPARAÇÃO {'='*20}")
    print(f"Número que funciona: {working_number} -> {formatted_working}")
    print(f"Número que não funciona: {failing_number} -> {formatted_failing}")
    
    # Verificar diferenças
    if formatted_working == formatted_failing:
        print("✅ Ambos têm o mesmo formato!")
        print("❌ O problema não é na formatação")
    else:
        print("❌ Formatos diferentes!")
        print("✅ O problema pode ser na formatação")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")

if __name__ == "__main__":
    test_both_numbers() 