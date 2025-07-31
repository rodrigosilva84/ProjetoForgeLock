#!/usr/bin/env python
"""
Script para padronizar traduções automaticamente.
Remove duplicatas, padroniza labels e otimiza arquivos .po
"""

import os
import sys
import polib
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def standardize_po_file(po_file_path):
    """Padroniza um arquivo .po específico"""
    print(f"\nPadronizando: {po_file_path}")
    
    try:
        po = polib.pofile(po_file_path)
        original_count = len(po)
        
        # Remover duplicatas
        seen_msgids = set()
        entries_to_remove = []
        
        for entry in po:
            if entry.msgid in seen_msgids:
                entries_to_remove.append(entry)
            else:
                seen_msgids.add(entry.msgid)
        
        # Remover entradas duplicadas
        for entry in entries_to_remove:
            po.remove(entry)
        
        # Salvar arquivo padronizado
        po.save()
        
        removed_count = len(entries_to_remove)
        final_count = len(po)
        
        print(f"   SUCCESS: Removidas {removed_count} duplicatas")
        print(f"   INFO: Antes: {original_count}, Depois: {final_count}")
        
        return removed_count
        
    except Exception as e:
        print(f"ERROR: Erro ao padronizar {po_file_path}: {e}")
        return 0

def main():
    """Função principal"""
    print("Padronizador de Traduções - ForgeLock")
    print("=" * 50)
    
    locale_dir = Path("locale")
    if not locale_dir.exists():
        print("ERROR: Diretório 'locale' não encontrado!")
        return
    
    total_removed = 0
    files_processed = 0
    
    # Processar arquivos .po em todos os idiomas
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir():
            po_file = lang_dir / "LC_MESSAGES" / "django.po"
            if po_file.exists():
                files_processed += 1
                total_removed += standardize_po_file(str(po_file))
    
    print("\n" + "=" * 50)
    print(f"Resumo:")
    print(f"   Arquivos processados: {files_processed}")
    print(f"   Total de duplicatas removidas: {total_removed}")
    
    if total_removed > 0:
        print("\nPróximos passos:")
        print("   - Execute: python manage.py compilemessages")
        print("   - Teste as traduções no site")
        print("   - Use django-rosetta para traduzir strings faltantes")
    else:
        print("SUCCESS: Nenhuma duplicata encontrada!")

if __name__ == "__main__":
    main() 