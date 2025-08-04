#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Plan, PlanPrice

def add_multicurrency_prices():
    print("=== ADICIONANDO PREÇOS MULTIMOEDA ===\n")
    
    # Obter planos Básico e Premium
    basic_plan = Plan.objects.get(name='Básico')
    premium_plan = Plan.objects.get(name='Premium')
    
    # Preços em USD (aproximadamente 1 USD = 5.5 BRL)
    print("💰 ADICIONANDO PREÇOS USD:")
    
    # Basic USD
    PlanPrice.objects.get_or_create(
        plan=basic_plan,
        currency='USD',
        defaults={
            'price': 12.99,  # ~R$ 70 / 5.5
            'yearly_price': 129.99,  # ~R$ 700 / 5.5
            'is_active': True
        }
    )
    print("   ✅ Basic USD criado")
    
    # Premium USD
    PlanPrice.objects.get_or_create(
        plan=premium_plan,
        currency='USD',
        defaults={
            'price': 21.99,  # ~R$ 119 / 5.5
            'yearly_price': 219.99,  # ~R$ 1190 / 5.5
            'is_active': True
        }
    )
    print("   ✅ Premium USD criado")
    
    # Preços em EUR (aproximadamente 1 EUR = 6 BRL)
    print("\n💰 ADICIONANDO PREÇOS EUR:")
    
    # Basic EUR
    PlanPrice.objects.get_or_create(
        plan=basic_plan,
        currency='EUR',
        defaults={
            'price': 11.99,  # ~R$ 70 / 6
            'yearly_price': 119.99,  # ~R$ 700 / 6
            'is_active': True
        }
    )
    print("   ✅ Basic EUR criado")
    
    # Premium EUR
    PlanPrice.objects.get_or_create(
        plan=premium_plan,
        currency='EUR',
        defaults={
            'price': 19.99,  # ~R$ 119 / 6
            'yearly_price': 199.99,  # ~R$ 1190 / 6
            'is_active': True
        }
    )
    print("   ✅ Premium EUR criado")
    
    print()
    
    # Verificar resultado
    print("📊 PREÇOS FINAIS:")
    for plan in [basic_plan, premium_plan]:
        print(f"\n   • {plan.name}:")
        prices = PlanPrice.objects.filter(plan=plan, is_active=True)
        for price in prices:
            print(f"     - {price.currency}: ${price.price} mensal, ${price.yearly_price} anual")
    
    print("\n=== PREÇOS MULTIMOEDA ADICIONADOS ===")

if __name__ == "__main__":
    add_multicurrency_prices() 