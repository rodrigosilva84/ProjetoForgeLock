#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import User, Company

def clean_companies():
    print("=== LIMPEZA DE EMPRESAS ===\n")
    
    # 1. Remover empresas sem usuários
    companies_without_users = Company.objects.filter(user__isnull=True)
    print(f"🗑️  REMOVENDO EMPRESAS SEM USUÁRIOS:")
    for company in companies_without_users:
        print(f"   • Removendo: {company.name} (ID: {company.id})")
        company.delete()
    print(f"   ✅ Removidas {companies_without_users.count()} empresas sem usuários")
    print()
    
    # 2. Verificar empresas duplicadas
    print(f"🔍 VERIFICANDO EMPRESAS DUPLICADAS:")
    companies = Company.objects.all()
    company_names = {}
    
    for company in companies:
        if company.name in company_names:
            company_names[company.name].append(company)
        else:
            company_names[company.name] = [company]
    
    duplicates = {name: companies for name, companies in company_names.items() if len(companies) > 1}
    
    if duplicates:
        print(f"   ⚠️  ENCONTRADAS EMPRESAS DUPLICADAS:")
        for name, companies_list in duplicates.items():
            print(f"   • '{name}' aparece {len(companies_list)} vezes:")
            for company in companies_list:
                users_count = company.user_set.count()
                print(f"     - ID {company.id}: {users_count} usuário(s)")
        
        print(f"   💡 SUGESTÃO: Manter apenas a empresa com usuários, remover as vazias")
    else:
        print(f"   ✅ Nenhuma empresa duplicada encontrada")
    
    print()
    
    # 3. Relatório final
    print(f"📊 RELATÓRIO FINAL:")
    total_users = User.objects.count()
    total_companies = Company.objects.count()
    print(f"   • Usuários: {total_users}")
    print(f"   • Empresas: {total_companies}")
    
    if total_companies == total_users:
        print(f"   ✅ RELAÇÃO EQUILIBRADA!")
    else:
        print(f"   ⚠️  Ainda há inconsistências")
    
    print()
    print("=== FIM DA LIMPEZA ===")

if __name__ == "__main__":
    clean_companies() 