#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Plan, PlanPrice

def fix_plan_name():
    print("=== CORRIGINDO NOME DO PLANO ===\n")
    
    # Buscar o plano "Básico"
    basico_plan = Plan.objects.filter(name='Básico').first()
    
    if basico_plan:
        print(f"📝 PLANO ENCONTRADO:")
        print(f"   - Nome atual: {basico_plan.name}")
        print(f"   - Descrição: {basico_plan.description}")
        print(f"   - Usuários: {basico_plan.max_users}")
        print(f"   - STL Protection: {'Sim' if basico_plan.has_stl_security else 'Não'}")
        
        # Atualizar o nome
        basico_plan.name = 'Basic'
        basico_plan.save()
        
        print(f"\n✅ NOME CORRIGIDO:")
        print(f"   - Novo nome: {basico_plan.name}")
        
        # Verificar preços
        prices = PlanPrice.objects.filter(plan=basico_plan, is_active=True)
        print(f"\n💰 PREÇOS MANTIDOS:")
        for price in prices:
            symbol = {'BRL': 'R$', 'USD': '$', 'EUR': '€'}.get(price.currency, price.currency)
            print(f"   - {price.currency}: {symbol}{price.price} mensal, {symbol}{price.yearly_price} anual")
        
        print("\n=== CORREÇÃO CONCLUÍDA ===")
        
    else:
        print("❌ Plano 'Básico' não encontrado!")
        print("\n📊 PLANOS ATUAIS:")
        for plan in Plan.objects.filter(is_active=True).order_by('name'):
            print(f"   - {plan.name}")

if __name__ == "__main__":
    fix_plan_name() 