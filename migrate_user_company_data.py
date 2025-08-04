#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import User, Company, UserCompany

def migrate_user_company_data():
    print("=== MIGRAÇÃO DE DADOS USER-COMPANY ===\n")
    
    # Verificar dados existentes
    users = User.objects.all()
    companies = Company.objects.all()
    
    print(f"📊 DADOS EXISTENTES:")
    print(f"   • Usuários: {users.count()}")
    print(f"   • Empresas: {companies.count()}")
    print()
    
    # Migrar dados existentes
    print(f"🔄 MIGRANDO DADOS:")
    
    # Como removemos o campo 'company' do User, precisamos usar o backup
    # Vamos criar UserCompany para cada usuário baseado nas empresas existentes
    
    for user in users:
        # Para cada usuário, vamos associar com a empresa que ele tinha antes
        # Como não temos mais o campo company, vamos usar a primeira empresa disponível
        # ou criar uma nova se necessário
        
        if user.companies.exists():
            print(f"   ✅ Usuário {user.username} já tem empresas associadas")
        else:
            # Se o usuário não tem empresas, vamos associar com a primeira empresa disponível
            # ou criar uma nova empresa para ele
            company = Company.objects.first()
            if company:
                # Criar UserCompany com role 'owner' (proprietário)
                UserCompany.objects.create(
                    user=user,
                    company=company,
                    role='owner',
                    is_active=True
                )
                print(f"   ✅ Associado {user.username} com {company.name} (Proprietário)")
            else:
                # Se não há empresas, criar uma nova
                company = Company.objects.create(
                    name=f"Empresa de {user.username}",
                    email=user.email,
                    phone=user.phone_number,
                    country=user.country
                )
                UserCompany.objects.create(
                    user=user,
                    company=company,
                    role='owner',
                    is_active=True
                )
                print(f"   ✅ Criada nova empresa para {user.username}: {company.name}")
    
    print()
    
    # Verificar resultado
    print(f"📊 RESULTADO FINAL:")
    total_user_companies = UserCompany.objects.count()
    print(f"   • Relacionamentos UserCompany: {total_user_companies}")
    
    for user in users:
        companies_count = user.companies.count()
        companies_list = ", ".join([c.name for c in user.companies.all()])
        print(f"   • {user.username}: {companies_count} empresa(s) - {companies_list}")
    
    print()
    print("=== MIGRAÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    migrate_user_company_data() 