#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Plan, PlanPrice

def restore_plans():
    print("=== RESTAURANDO PLANOS ADMIN E VITALÍCIO ===\n")
    
    # Criar plano Admin
    admin_plan = Plan.objects.create(
        name='Admin',
        description='Plano administrativo com acesso total',
        price=199.99,
        max_users=10,
        max_companies=5,
        max_customers=1000,
        max_products=500,
        max_projects=100,
        has_stl_security=True,
        is_trial=False,
        is_active=True
    )
    print("   ✅ Admin criado")
    
    # Criar plano Vitalício
    vitalicio_plan = Plan.objects.create(
        name='Vitalício',
        description='Plano vitalício com acesso permanente',
        price=999.99,
        max_users=50,
        max_companies=20,
        max_customers=10000,
        max_products=5000,
        max_projects=1000,
        has_stl_security=True,
        is_trial=False,
        is_active=True
    )
    print("   ✅ Vitalício criado")
    
    # Corrigir valores dos planos existentes
    print("\n🔧 CORRIGINDO VALORES DOS PLANOS EXISTENTES:")
    
    # Trial
    trial_plan = Plan.objects.get(name='Trial')
    trial_plan.max_customers = 50
    trial_plan.max_products = 10
    trial_plan.max_projects = 5
    trial_plan.save()
    print("   ✅ Trial corrigido")
    
    # Basic
    basic_plan = Plan.objects.get(name='Basic')
    basic_plan.max_customers = 1000  # Sem limite = 1000
    basic_plan.max_products = 500    # Sem limite = 500
    basic_plan.max_projects = 100    # Sem limite = 100
    basic_plan.save()
    print("   ✅ Basic corrigido")
    
    # Premium
    premium_plan = Plan.objects.get(name='Premium')
    premium_plan.max_customers = 10000  # Sem limite = 10000
    premium_plan.max_products = 5000    # Sem limite = 5000
    premium_plan.max_projects = 1000    # Sem limite = 1000
    premium_plan.save()
    print("   ✅ Premium corrigido")
    
    print()
    
    # Criar preços para os novos planos
    print("💰 CRIANDO PREÇOS:")
    
    # Admin
    PlanPrice.objects.get_or_create(
        plan=admin_plan,
        currency='BRL',
        defaults={
            'price': 199.99,
            'yearly_price': 1999.99,  # 10 meses (2 grátis)
            'is_active': True
        }
    )
    print("   ✅ Preços Admin criados")
    
    # Vitalício
    PlanPrice.objects.get_or_create(
        plan=vitalicio_plan,
        currency='BRL',
        defaults={
            'price': 999.99,
            'yearly_price': 9999.99,  # 10 meses (2 grátis)
            'is_active': True
        }
    )
    print("   ✅ Preços Vitalício criados")
    
    print()
    
    # Verificar resultado
    print("📊 PLANOS FINAIS:")
    for plan in Plan.objects.filter(is_active=True).order_by('price'):
        print(f"   • {plan.name}:")
        print(f"     - Usuários: {plan.max_users}")
        print(f"     - Empresas: {plan.max_companies}")
        print(f"     - Clientes: {plan.max_customers}")
        print(f"     - Produtos: {plan.max_products}")
        print(f"     - Projetos: {plan.max_projects}")
        print(f"     - STL Security: {'Sim' if plan.has_stl_security else 'Não'}")
        print(f"     - Preço: R$ {plan.price}")
        print()
    
    print("=== RESTAURAÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    restore_plans() 