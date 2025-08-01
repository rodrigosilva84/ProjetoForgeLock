#!/usr/bin/env python
"""
Script para verificar o status do usuário rasilva84
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from core.models import User, Company

def check_user():
    """Verifica o status do usuário rasilva84"""
    print("Verificando usuário rasilva84...")
    
    try:
        user = User.objects.get(username='rasilva84')
        print(f"✅ Usuário encontrado: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Nome: {user.first_name} {user.last_name}")
        print(f"   Ativo: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        
        # Verificar empresa
        if user.company:
            print(f"   Empresa: {user.company.name} (ID: {user.company.id})")
        else:
            print("   Empresa: Nenhuma empresa associada")
            
        # Verificar se consegue fazer login
        print(f"\nTestando login...")
        from django.contrib.auth import authenticate
        auth_user = authenticate(username='rasilva84', password='test123')
        if auth_user:
            print("✅ Login funcionando!")
        else:
            print("❌ Login falhou!")
            
    except User.DoesNotExist:
        print("❌ Usuário rasilva84 não encontrado!")
        
        # Listar todos os usuários
        print("\nUsuários existentes:")
        for u in User.objects.all():
            print(f"  - {u.username} ({u.email})")

if __name__ == "__main__":
    check_user() 