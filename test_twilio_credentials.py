#!/usr/bin/env python
"""
Script para testar credenciais do Twilio
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from django.conf import settings

def test_twilio_credentials():
    """Testa se as credenciais do Twilio estão configuradas"""
    print("Teste de Credenciais do Twilio")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    print(f"TWILIO_ACCOUNT_SID: {'✅ Configurado' if settings.TWILIO_ACCOUNT_SID else '❌ Não configurado'}")
    print(f"TWILIO_AUTH_TOKEN: {'✅ Configurado' if settings.TWILIO_AUTH_TOKEN else '❌ Não configurado'}")
    print(f"TWILIO_VERIFY_SERVICE_SID: {'✅ Configurado' if settings.TWILIO_VERIFY_SERVICE_SID else '❌ Não configurado'}")
    print(f"SMS_DEVELOPMENT_MODE: {'❌ Ativo (usando fallback)' if settings.SMS_DEVELOPMENT_MODE else '✅ Desabilitado (usando Twilio real)'}")
    
    # Testar conexão com Twilio
    if all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_VERIFY_SERVICE_SID]):
        print("\nTestando conexão com Twilio...")
        try:
            from twilio.rest import Client
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Tentar buscar informações da conta
            account = client.api.accounts(settings.TWILIO_ACCOUNT_SID).fetch()
            print(f"✅ Conexão bem-sucedida! Conta: {account.friendly_name}")
            
            # Testar serviço de verificação
            verify_service = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID).fetch()
            print(f"✅ Serviço de verificação: {verify_service.friendly_name}")
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
    else:
        print("\n❌ Credenciais incompletas!")
    
    print("\n" + "=" * 50)
    print("Teste concluído!")

if __name__ == "__main__":
    test_twilio_credentials() 