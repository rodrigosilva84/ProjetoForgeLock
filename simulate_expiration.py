#!/usr/bin/env python
"""
Script para simular expiração de assinatura
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from django.utils import timezone
from core.models import User, Subscription

def simulate_expiration():
    """Simula a expiração da assinatura do usuário pato_donald"""
    
    try:
        # Buscar o usuário
        user = User.objects.get(username='pato_donald')
        print(f"✅ Usuário encontrado: {user.email}")
        
        # Buscar a assinatura ativa
        subscription = user.subscriptions.filter(status__in=['trial', 'active']).first()
        
        if not subscription:
            print("❌ Nenhuma assinatura ativa encontrada")
            return
        
        print(f"📅 Assinatura atual: {subscription.plan.name} - Status: {subscription.status}")
        print(f"📅 Data de fim atual: {subscription.end_date}")
        
        # Simular expiração (definir data de fim para ontem)
        yesterday = timezone.now() - timedelta(days=1)
        subscription.end_date = yesterday
        subscription.status = 'expired'
        subscription.save()
        
        print(f"🔴 Assinatura expirada! Nova data de fim: {subscription.end_date}")
        print(f"🔴 Status alterado para: {subscription.status}")
        
        # Executar comando de verificação para mover para período de carência
        print("\n🔄 Executando verificação de assinaturas...")
        os.system('python manage.py check_subscriptions')
        
        print("\n✅ Simulação concluída!")
        print("💡 Agora teste acessando o dashboard e as páginas protegidas")
        
    except User.DoesNotExist:
        print("❌ Usuário 'pato_donald' não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

def reset_subscription():
    """Reseta a assinatura para trial ativo"""
    
    try:
        user = User.objects.get(username='pato_donald')
        subscription = user.subscriptions.filter(status__in=['trial', 'active', 'expired', 'grace_period']).first()
        
        if subscription:
            # Resetar para trial ativo
            subscription.status = 'trial'
            subscription.end_date = timezone.now() + timedelta(days=15)
            subscription.grace_period_until = None
            subscription.save()
            
            print(f"✅ Assinatura resetada para trial ativo!")
            print(f"📅 Nova data de fim: {subscription.end_date}")
        
    except User.DoesNotExist:
        print("❌ Usuário 'pato_donald' não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        print("🔄 Resetando assinatura...")
        reset_subscription()
    else:
        print("🔴 Simulando expiração da assinatura...")
        simulate_expiration() 