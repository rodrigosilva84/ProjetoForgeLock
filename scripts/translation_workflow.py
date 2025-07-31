#!/usr/bin/env python
"""
Workflow completo de tradução automática.
Detecta, traduz, valida e compila traduções automaticamente.
"""

import os
import sys
import subprocess
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n{description}")
    print(f"   Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("   SUCCESS!")
            if result.stdout:
                print(f"   Saída: {result.stdout.strip()}")
        else:
            print(f"   ERROR: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"   ERROR: Erro ao executar comando: {e}")
        return False
    
    return True

def main():
    """Workflow completo de tradução"""
    print("Workflow de Tradução Automática - ForgeLock")
    print("=" * 60)
    
    # 1. Detectar novas strings
    print("\nPasso 1: Detectando novas strings...")
    if not run_command("python manage.py makemessages -l en -l es", "Detectando strings"):
        return
    
    # 2. Validar traduções atuais
    print("\nPasso 2: Validando traduções atuais...")
    if not run_command("python scripts/validate_translations.py", "Validando traduções"):
        return
    
    # 3. Traduzir automaticamente
    print("\nPasso 3: Traduzindo automaticamente...")
    if not run_command("python scripts/auto_translate.py", "Tradução automática"):
        return
    
    # 4. Padronizar traduções
    print("\nPasso 4: Padronizando traduções...")
    if not run_command("python scripts/standardize_translations.py", "Padronização"):
        return
    
    # 5. Compilar mensagens
    print("\nPasso 5: Compilando mensagens...")
    if not run_command("python manage.py compilemessages", "Compilação"):
        return
    
    # 6. Validação final
    print("\nPasso 6: Validação final...")
    if not run_command("python scripts/validate_translations.py", "Validação final"):
        return
    
    print("\n" + "=" * 60)
    print("SUCCESS: Workflow de tradução concluído com sucesso!")
    print("\nPróximos passos:")
    print("   - Teste as traduções no site")
    print("   - Revise traduções que precisam de ajuste")
    print("   - Execute este workflow sempre que adicionar novas strings")

if __name__ == "__main__":
    main() 