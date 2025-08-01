#!/usr/bin/env python
"""
Script para criar um novo usuário de teste
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import User, Country

def create_test_user():
    """Cria um usuário de teste"""
    print("Criando usuário de teste...")
    
    # Verificar se já existe um usuário
    if User.objects.exists():
        print("Usuários existentes:")
        for user in User.objects.all():
            print(f"  - {user.username} ({user.email})")
        return
    
    # Buscar um país para usar como padrão
    try:
        country = Country.objects.filter(is_active=True).first()
        if not country:
            print("❌ Nenhum país ativo encontrado!")
            return
    except Exception as e:
        print(f"❌ Erro ao buscar país: {e}")
        return
    
    # Criar usuário de teste
    try:
        user = User.objects.create_user(
            username='rasilva84',
            email='rasilva84@test.com',
            password='test123',
            first_name='Rafael',
            last_name='Silva',
            phone_number='(11) 99999-9999',
            country=country,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        
        print(f"✅ Usuário criado com sucesso!")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Senha: test123")
        print(f"   País: {user.country.name}")
        print(f"   Admin: Sim")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")

if __name__ == "__main__":
    create_test_user() 