#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import User, UserCompany, Company

# Associar tech_admin à empresa Pato Donald
try:
    tech_admin = User.objects.get(username='tech_admin')
    pato_donald_company = Company.objects.get(name='Pato Donald')
    
    # Verificar se já existe associação
    existing_association = UserCompany.objects.filter(
        user=tech_admin, 
        company=pato_donald_company
    ).first()
    
    if existing_association:
        print(f"Associação já existe: {tech_admin.username} -> {pato_donald_company.name}")
        print(f"Role: {existing_association.role}, Ativo: {existing_association.is_active}")
    else:
        # Criar nova associação
        UserCompany.objects.create(
            user=tech_admin,
            company=pato_donald_company,
            role='admin',  # Dar permissão de admin
            is_active=True
        )
        print(f"Associação criada: {tech_admin.username} -> {pato_donald_company.name}")
    
    # Verificar todas as associações do tech_admin
    print(f"\nTodas as associações do {tech_admin.username}:")
    for uc in UserCompany.objects.filter(user=tech_admin):
        print(f"  - {uc.company.name} (role: {uc.role}, ativo: {uc.is_active})")
        
except User.DoesNotExist:
    print("Usuário tech_admin não encontrado")
except Company.DoesNotExist:
    print("Empresa Pato Donald não encontrada")
