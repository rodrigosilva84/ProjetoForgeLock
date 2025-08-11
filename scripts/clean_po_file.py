#!/usr/bin/env python3
"""
Limpador Completo de Arquivo PO - ForgeLock
Remove todas as duplicatas e problemas de um arquivo PO
"""
import re
from pathlib import Path
from collections import defaultdict

def clean_po_file(po_file_path):
    """Limpa completamente o arquivo PO"""
    try:
        print(f"🔍 Processando: {po_file_path.name}")
        
        # Ler arquivo
        with open(po_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Separar em entradas
        entries = re.split(r'\n\n', content)
        
        # Manter apenas o header
        header = entries[0]
        
        # Processar entradas de tradução
        unique_entries = []
        seen_msgids = set()
        
        for entry in entries[1:]:
            if not entry.strip():
                continue
                
            # Extrair msgid
            msgid_match = re.search(r'^msgid "(.*)"$', entry, re.MULTILINE)
            if not msgid_match:
                continue
                
            msgid = msgid_match.group(1)
            
            # Pular entradas vazias (header)
            if msgid == "":
                continue
                
            # Se já vimos este msgid, pular
            if msgid in seen_msgids:
                print(f"   🗑️  Duplicata removida: '{msgid}'")
                continue
                
            seen_msgids.add(msgid)
            unique_entries.append(entry)
        
        # Reconstruir arquivo
        cleaned_content = header + "\n\n" + "\n\n".join(unique_entries)
        
        # Salvar arquivo limpo
        with open(po_file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"   ✅ Arquivo limpo: {len(unique_entries)} entradas únicas mantidas")
        return len(unique_entries)
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return 0

def main():
    print("🧹 Limpador Completo de Arquivo PO - ForgeLock")
    print("=" * 50)
    
    locale_dir = Path("locale")
    total_entries = 0
    
    # Processar português (que tem problemas)
    po_file = locale_dir / "pt" / "LC_MESSAGES" / "django.po"
    if po_file.exists():
        entries = clean_po_file(po_file)
        total_entries += entries
    
    print(f"\n📊 Total de entradas únicas: {total_entries}")
    
    if total_entries > 0:
        print("✅ Execute: python manage.py compilemessages")
    
    return total_entries > 0

if __name__ == "__main__":
    main()

