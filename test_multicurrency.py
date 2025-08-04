#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.views import home
from django.test import RequestFactory

def test_multicurrency():
    print("=== TESTE DE SIMULAÇÃO MULTIMOEDA ===\n")
    
    rf = RequestFactory()
    
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
        
        # Criar request com simulação
        request = rf.get(f'/?simulate={country_code}')
        
        # Chamar view
        response = home(request)
        
        # Extrair dados do contexto
        if hasattr(response, 'context_data'):
            context = response.context_data
        else:
            # Para HttpResponse, tentar acessar o contexto de outra forma
            print(f"   Status: {response.status_code}")
            print(f"   Erro: Não foi possível acessar o contexto")
            continue
            
        user_currency = context.get('user_currency')
        user_currency_symbol = context.get('user_currency_symbol')
        plans = context.get('plans')
        
        print(f"   Moeda detectada: {user_currency} ({user_currency_symbol})")
        print(f"   Planos encontrados: {len(plans)}")
        
        # Mostrar preços dos planos
        for plan in plans:
            try:
                monthly_price = plan.get_price_for_currency(user_currency, 'monthly')
                yearly_price = plan.get_yearly_price(user_currency)
                print(f"   - {plan.name}: {user_currency_symbol}{monthly_price} mensal, {user_currency_symbol}{yearly_price} anual")
            except Exception as e:
                print(f"   - {plan.name}: Erro ao obter preço - {e}")
        
        print()

if __name__ == "__main__":
    test_multicurrency() 