#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.services import GeolocationService
from core.models import Plan, PlanPrice

def test_simple_multicurrency():
    print("=== TESTE SIMPLES DE MULTIMOEDA ===\n")
    
    # Testar diferentes regiões
    regions = [
        ('BR', 'Brasil - BRL'),
        ('US', 'Estados Unidos - USD'),
        ('DE', 'Alemanha - EUR'),
        ('FR', 'França - EUR'),
        ('GB', 'Reino Unido - USD'),
    ]
    
    for country_code, description in regions:
        print(f"🌍 {description}:")
        
        # Simular detecção de moeda
        currency = GeolocationService.get_currency_by_country(country_code)
        currency_symbol = {
            'BRL': 'R$',
            'USD': '$',
            'EUR': '€'
        }.get(currency, currency)
        
        print(f"   Moeda detectada: {currency} ({currency_symbol})")
        
        # Buscar planos Basic e Premium
        plans = Plan.objects.filter(name__in=['Básico', 'Premium'])
        
        for plan in plans:
            try:
                # Buscar preço na moeda
                price_obj = PlanPrice.objects.get(plan=plan, currency=currency, is_active=True)
                print(f"   - {plan.name}: {currency_symbol}{price_obj.price} mensal, {currency_symbol}{price_obj.yearly_price} anual")
            except PlanPrice.DoesNotExist:
                print(f"   - {plan.name}: Preço não encontrado para {currency}")
        
        print()

if __name__ == "__main__":
    test_simple_multicurrency() 