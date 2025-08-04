#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import Plan, PlanPrice, User, Account

def restructure_plans():
    print("=== REESTRUTURAÇÃO DOS PLANOS ===\n")
    
    # 1. Deletar planos antigos (exceto Trial temporariamente)
    print("🗑️  REMOVENDO PLANOS ANTIGOS:")
    old_plans = Plan.objects.exclude(name__iexact='trial')
    for plan in old_plans:
        print(f"   - Removendo: {plan.name}")
    old_plans.delete()
    print("   ✅ Planos antigos removidos")
    
    # 2. Criar novos planos
    print("\n📝 CRIANDO NOVOS PLANOS:")
    
    # Básico
    basico_plan = Plan.objects.create(
        name='Básico',
        description='Ideal para quem transforma arquivos digitais em arte física. Gerencie sua produção e suas vendas de forma simples e eficiente, sem se preocupar com limites de clientes ou projetos.',
        max_users=1,
        max_companies=1,
        max_customers=0,  # Ilimitado
        max_products=0,    # Ilimitado
        max_projects=0,    # Ilimitado
        has_stl_security=False,
        is_trial=False,
        is_active=True
    )
    print("   ✅ Básico criado")
    
    # Pro
    pro_plan = Plan.objects.create(
        name='Pro',
        description='A solução completa para quem vive de criar arquivos 3D. Proteja seu portfólio digital contra pirataria, garanta a exclusividade de suas criações e gerencie seu negócio com segurança.',
        max_users=1,
        max_companies=1,
        max_customers=0,  # Ilimitado
        max_products=0,   # Ilimitado
        max_projects=0,   # Ilimitado
        has_stl_security=True,
        is_trial=False,
        is_active=True
    )
    print("   ✅ Pro criado")
    
    # Enterprise
    enterprise_plan = Plan.objects.create(
        name='Enterprise',
        description='Feito para equipes que criam e comercializam em grande escala. Organize a gestão de projetos com até 5 usuários, centralize a comunicação e proteja os arquivos digitais da sua empresa contra pirataria.',
        max_users=5,
        max_companies=1,
        max_customers=0,  # Ilimitado
        max_products=0,   # Ilimitado
        max_projects=0,   # Ilimitado
        has_stl_security=True,
        is_trial=False,
        is_active=True
    )
    print("   ✅ Enterprise criado")
    
    # 3. Criar preços para todos os planos
    print("\n💰 CRIANDO PREÇOS:")
    
    plans_and_prices = [
        (basico_plan, 69.99, 699.99),    # BRL
        (pro_plan, 119.99, 1199.99),     # BRL
        (enterprise_plan, 249.99, 2499.99), # BRL
    ]
    
    for plan, monthly_price, yearly_price in plans_and_prices:
        # BRL
        PlanPrice.objects.get_or_create(
            plan=plan,
            currency='BRL',
            defaults={
                'price': monthly_price,
                'yearly_price': yearly_price,
                'is_active': True
            }
        )
        
        # USD (conversão direta: 1 BRL = 0.2 USD)
        PlanPrice.objects.get_or_create(
            plan=plan,
            currency='USD',
            defaults={
                'price': round(monthly_price * 0.2, 2),
                'yearly_price': round(yearly_price * 0.2, 2),
                'is_active': True
            }
        )
        
        # EUR (conversão direta: 1 BRL = 0.18 EUR)
        PlanPrice.objects.get_or_create(
            plan=plan,
            currency='EUR',
            defaults={
                'price': round(monthly_price * 0.18, 2),
                'yearly_price': round(yearly_price * 0.18, 2),
                'is_active': True
            }
        )
        
        print(f"   ✅ Preços criados para {plan.name}")
    
    # 4. Migrar usuários existentes para Enterprise
    print("\n👥 MIGRANDO USUÁRIOS EXISTENTES:")
    
    # Buscar usuários que têm conta
    users_with_accounts = User.objects.filter(account__isnull=False)
    users_without_accounts = User.objects.filter(account__isnull=True)
    
    print(f"   Usuários com conta: {users_with_accounts.count()}")
    print(f"   Usuários sem conta: {users_without_accounts.count()}")
    
    # Atualizar contas existentes para Enterprise
    for user in users_with_accounts:
        try:
            account = user.account
            account.plan = enterprise_plan
            account.save()
            print(f"   ✅ {user.username} migrado para Enterprise")
        except Exception as e:
            print(f"   ❌ Erro ao migrar {user.username}: {e}")
    
    # Criar contas Enterprise para usuários sem conta
    for user in users_without_accounts:
        try:
            Account.objects.create(
                user=user,
                plan=enterprise_plan,
                is_active=True
            )
            print(f"   ✅ Conta Enterprise criada para {user.username}")
        except Exception as e:
            print(f"   ❌ Erro ao criar conta para {user.username}: {e}")
    
    # 5. Remover plano Trial (não será mais usado)
    print("\n🗑️  REMOVENDO PLANO TRIAL:")
    trial_plan = Plan.objects.filter(name__iexact='trial').first()
    if trial_plan:
        trial_plan.delete()
        print("   ✅ Plano Trial removido")
    
    print()
    
    # 6. Verificar resultado final
    print("📊 ESTRUTURA FINAL:")
    for plan in Plan.objects.filter(is_active=True).order_by('name'):
        print(f"\n   • {plan.name}:")
        print(f"     - Usuários: {plan.max_users}")
        print(f"     - STL Protection: {'Sim' if plan.has_stl_security else 'Não'}")
        print(f"     - Limites: Ilimitado")
        
        prices = PlanPrice.objects.filter(plan=plan, is_active=True)
        for price in prices:
            symbol = {'BRL': 'R$', 'USD': '$', 'EUR': '€'}.get(price.currency, price.currency)
            print(f"     - {price.currency}: {symbol}{price.price} mensal, {symbol}{price.yearly_price} anual")
    
    print("\n=== REESTRUTURAÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    restructure_plans() 