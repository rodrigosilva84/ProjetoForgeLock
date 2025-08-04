#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import User, Company, UserCompany

def check_users_companies():
    print("=== VERIFICAÇÃO DE USUÁRIOS E EMPRESAS ===\n")
    
    # Contar usuários e empresas
    total_users = User.objects.count()
    total_companies = Company.objects.count()
    
    print(f"📊 ESTATÍSTICAS GERAIS:")
    print(f"   • Total de usuários: {total_users}")
    print(f"   • Total de empresas: {total_companies}")
    print()
    
    # Usuários com empresas (usando o novo sistema)
    users_with_companies = User.objects.filter(companies__isnull=False).distinct().count()
    users_without_companies = User.objects.filter(companies__isnull=True).count()
    
    print(f"👥 USUÁRIOS:")
    print(f"   • Com empresas: {users_with_companies}")
    print(f"   • Sem empresas: {users_without_companies}")
    print()
    
    # Empresas com usuários (usando o novo sistema)
    companies_with_users = Company.objects.filter(user__isnull=False).distinct().count()
    companies_without_users = Company.objects.filter(user__isnull=True).count()
    
    print(f"🏢 EMPRESAS:")
    print(f"   • Com usuários: {companies_with_users}")
    print(f"   • Sem usuários: {companies_without_users}")
    print()
    
    # Detalhes dos usuários
    print(f"📋 DETALHES DOS USUÁRIOS:")
    for user in User.objects.all():
        companies_count = user.companies.count()
        companies_list = ", ".join([c.name for c in user.companies.all()])
        print(f"   • {user.username} ({user.email}) → {companies_count} empresa(s): {companies_list}")
    print()
    
    # Detalhes das empresas
    print(f"📋 DETALHES DAS EMPRESAS:")
    for company in Company.objects.all():
        users_count = company.user_set.count()
        users_list = ", ".join([user.username for user in company.user_set.all()])
        print(f"   • {company.name} → {users_count} usuário(s): {users_list}")
    print()
    
    # Detalhes dos relacionamentos UserCompany
    print(f"🔗 DETALHES DOS RELACIONAMENTOS USER-COMPANY:")
    for uc in UserCompany.objects.all():
        print(f"   • {uc.user.username} → {uc.company.name} (Role: {uc.get_role_display()})")
    print()
    
    # Análise da relação
    print(f"🔍 ANÁLISE DA RELAÇÃO:")
    if total_companies > total_users:
        print(f"   ⚠️  PROBLEMA: Mais empresas ({total_companies}) que usuários ({total_users})")
        print(f"   💡 SUGESTÃO: Empresas sem usuários podem ser removidas ou precisam de usuários")
    elif total_users > total_companies:
        print(f"   ⚠️  PROBLEMA: Mais usuários ({total_users}) que empresas ({total_companies})")
        print(f"   💡 SUGESTÃO: Usuários sem empresa precisam ser associados a uma empresa")
    else:
        print(f"   ✅ RELAÇÃO EQUILIBRADA: {total_users} usuários e {total_companies} empresas")
    
    print()
    print("=== FIM DA VERIFICAÇÃO ===")

if __name__ == "__main__":
    check_users_companies() 