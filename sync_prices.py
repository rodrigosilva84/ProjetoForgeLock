#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Plan, PlanPrice

def sync_prices():
    print("=== SINCRONIZANDO PREÇOS ===\n")
    
    # Definir preços corretos
    plan_prices = {
        'Trial': {'monthly': 0, 'yearly': 0},
        'Basic': {'monthly': 70.00, 'yearly': 700.00},
        'Premium': {'monthly': 119.00, 'yearly': 1190.00},
        'Admin': {'monthly': 199.99, 'yearly': 1999.99},
        'Vitalício': {'monthly': 999.99, 'yearly': 9999.99},
    }
    
    for plan_name, prices in plan_prices.items():
        try:
            plan = Plan.objects.get(name=plan_name)
            
            # Atualizar preço no modelo Plan
            plan.price = prices['monthly']
            plan.save()
            
            # Atualizar preços no PlanPrice
            plan_price, created = PlanPrice.objects.get_or_create(
                plan=plan,
                currency='BRL',
                defaults={
                    'price': prices['monthly'],
                    'yearly_price': prices['yearly'],
                    'is_active': True
                }
            )
            
            if not created:
                plan_price.price = prices['monthly']
                plan_price.yearly_price = prices['yearly']
                plan_price.save()
            
            print(f"   ✅ {plan_name}: R$ {prices['monthly']} (mensal), R$ {prices['yearly']} (anual)")
            
        except Plan.DoesNotExist:
            print(f"   ❌ Plano {plan_name} não encontrado")
    
    print("\n=== SINCRONIZAÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    sync_prices() 