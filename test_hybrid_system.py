#!/usr/bin/env python
"""
Script para testar o sistema híbrido SMS/fallback
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.services import VerificationService

def test_hybrid_system():
    """Testa o sistema híbrido"""
    print("Teste do Sistema Híbrido SMS/Fallback")
    print("=" * 50)
    
    verification_service = VerificationService()
    
    # Números para testar
    verified_number = "+5517981839329"    # Verificado no Twilio
    unverified_number = "+5517981690470"  # Não verificado
    
    print(f"\n{'='*20} TESTANDO NÚMERO VERIFICADO {'='*20}")
    print(f"Enviando para: {verified_number}")
    result1 = verification_service.twilio_verify.send_verification(verified_number)
    print(f"Resultado: {'✅ SMS enviado' if result1 else '❌ Falhou'}")
    
    print(f"\n{'='*20} TESTANDO NÚMERO NÃO VERIFICADO {'='*20}")
    print(f"Enviando para: {unverified_number}")
    result2 = verification_service.twilio_verify.send_verification(unverified_number)
    print(f"Resultado: {'✅ Fallback usado' if result2 else '❌ Falhou'}")
    
    print(f"\n{'='*20} RESUMO {'='*20}")
    print(f"Número verificado: {'✅ Funcionou' if result1 else '❌ Falhou'}")
    print(f"Número não verificado: {'✅ Fallback funcionou' if result2 else '❌ Falhou'}")
    
    if result1 and result2:
        print("🎉 Sistema híbrido funcionando perfeitamente!")
    else:
        print("⚠️ Algum problema detectado")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")

if __name__ == "__main__":
    test_hybrid_system() 