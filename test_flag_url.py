#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

from django.templatetags.static import static
from django.conf import settings

def test_flag_url():
    """Testa se a URL da bandeira está funcionando"""
    print("=== TESTE DE URL DA BANDEIRA ===")
    
    # Testar com a bandeira da Itália
    flag_code = 'it'
    flag_path = f'images/flags/{flag_code}.svg'
    
    print(f"Flag code: {flag_code}")
    print(f"Flag path: {flag_path}")
    
    # Verificar se o arquivo existe
    full_path = os.path.join(settings.BASE_DIR, 'static', flag_path)
    print(f"Full path: {full_path}")
    print(f"File exists: {os.path.exists(full_path)}")
    
    # Testar URL estática
    static_url = static(flag_path)
    print(f"Static URL: {static_url}")
    
    # Verificar se o arquivo está no diretório correto
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    print(f"Static dir: {static_dir}")
    print(f"Static dir exists: {os.path.exists(static_dir)}")
    
    # Listar arquivos no diretório flags
    flags_dir = os.path.join(static_dir, 'images', 'flags')
    if os.path.exists(flags_dir):
        files = os.listdir(flags_dir)
        print(f"Files in flags dir: {files[:10]}...")  # Primeiros 10 arquivos
    else:
        print("Flags directory does not exist!")

if __name__ == "__main__":
    test_flag_url()
