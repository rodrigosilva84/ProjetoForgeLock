#!/usr/bin/env python
"""
Script para validar traduções automaticamente.
Detecta strings não traduzidas, duplicatas e problemas de qualidade.
"""

import os
import sys
import polib
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def validate_po_file(po_file_path):
    """Valida um arquivo .po específico"""
    print(f"\nValidando: {po_file_path}")
    
    try:
        po = polib.pofile(po_file_path)
        issues = []
        
        # Verificar strings vazias
        empty_strings = [entry for entry in po if not entry.msgstr.strip()]
        if empty_strings:
            issues.append(f"ERROR: {len(empty_strings)} strings sem tradução")
            for entry in empty_strings[:5]:  # Mostrar apenas as primeiras 5
                issues.append(f"   - {entry.msgid}")
        
        # Verificar duplicatas
        msgids = [entry.msgid for entry in po]
        duplicates = set([x for x in msgids if msgids.count(x) > 1])
        if duplicates:
            issues.append(f"ERROR: {len(duplicates)} msgids duplicados")
            for dup in list(duplicates)[:5]:
                issues.append(f"   - {dup}")
        
        # Verificar strings muito longas (possível problema)
        long_strings = [entry for entry in po if len(entry.msgid) > 100]
        if long_strings:
            issues.append(f"WARNING: {len(long_strings)} strings muito longas")
        
        if not issues:
            print("OK: Arquivo válido!")
        else:
            for issue in issues:
                print(issue)
                
        return len(empty_strings) + len(duplicates)
        
    except Exception as e:
        print(f"ERROR: Erro ao validar {po_file_path}: {e}")
        return 1

def main():
    """Função principal"""
    print("Validador de Traduções - ForgeLock")
    print("=" * 50)
    
    locale_dir = Path("locale")
    if not locale_dir.exists():
        print("ERROR: Diretório 'locale' não encontrado!")
        return
    
    total_issues = 0
    files_checked = 0
    
    # Verificar arquivos .po em todos os idiomas
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir():
            po_file = lang_dir / "LC_MESSAGES" / "django.po"
            if po_file.exists():
                files_checked += 1
                total_issues += validate_po_file(str(po_file))
    
    print("\n" + "=" * 50)
    print(f"Resumo:")
    print(f"   Arquivos verificados: {files_checked}")
    print(f"   Total de problemas: {total_issues}")
    
    if total_issues == 0:
        print("SUCCESS: Todas as traduções estão válidas!")
    else:
        print("WARNING: Encontrados problemas que precisam ser corrigidos.")
        print("\nDicas:")
        print("   - Execute: python manage.py compilemessages")
        print("   - Padronize labels nos templates")

if __name__ == "__main__":
    main() 