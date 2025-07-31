#!/usr/bin/env python
"""
Script para testar envio real via Twilio
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from django.conf import settings

def test_twilio_send():
    """Testa envio real via Twilio"""
    print("Teste de Envio Real via Twilio")
    print("=" * 50)
    
    # Números para testar
    working_number = "+5517981839329"  # Funciona
    failing_number = "+5517981690470"  # Não funciona
    
    if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_VERIFY_SERVICE_SID]):
        print("❌ Credenciais do Twilio não configuradas!")
        return
    
    try:
        from twilio.rest import Client
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        print(f"\n{'='*20} TESTANDO NÚMERO QUE FUNCIONA {'='*20}")
        print(f"Enviando para: {working_number}")
        
        try:
            verification = client.verify \
                .v2 \
                .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                .verifications \
                .create(to=working_number, channel='sms')
            
            print(f"✅ Sucesso! SID: {verification.sid}")
            print(f"Status: {verification.status}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        print(f"\n{'='*20} TESTANDO NÚMERO QUE NÃO FUNCIONA {'='*20}")
        print(f"Enviando para: {failing_number}")
        
        try:
            verification = client.verify \
                .v2 \
                .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                .verifications \
                .create(to=failing_number, channel='sms')
            
            print(f"✅ Sucesso! SID: {verification.sid}")
            print(f"Status: {verification.status}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            print(f"Tipo de erro: {type(e).__name__}")
            
            # Verificar se é erro específico do Twilio
            if hasattr(e, 'code'):
                print(f"Código de erro: {e.code}")
            if hasattr(e, 'msg'):
                print(f"Mensagem: {e.msg}")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")

if __name__ == "__main__":
    test_twilio_send() 