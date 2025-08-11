#!/usr/bin/env python3
"""
Corretor de Duplicatas - ForgeLock
Remove apenas as duplicatas restantes
"""

import polib
from pathlib import Path

def fix_duplicates_in_file(po_file_path):
    """Remove duplicatas de um arquivo .po específico"""
    try:
        print(f"🔍 Processando: {po_file_path.name}")
        
        po = polib.pofile(str(po_file_path))
        
        # Encontrar duplicatas
        seen_msgids = set()
        entries_to_remove = []
        
        for i, entry in enumerate(po):
            if entry.msgid and entry.msgid in seen_msgids:
                entries_to_remove.append(i)
                print(f"   🗑️  Duplicata encontrada: '{entry.msgid[:50]}...'")
            elif entry.msgid:
                seen_msgids.add(entry.msgid)
        
        # Remover duplicatas (em ordem reversa)
        for i in reversed(entries_to_remove):
            po.remove(po[i])
        
        if entries_to_remove:
            po.save(str(po_file_path))
            print(f"   ✅ {len(entries_to_remove)} duplicatas removidas")
        else:
            print(f"   ✅ Nenhuma duplicata encontrada")
        
        return len(entries_to_remove)
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return 0

def main():
    print("🔧 Corretor de Duplicatas - ForgeLock")
    print("=" * 50)
    
    locale_dir = Path("locale")
    total_removed = 0
    
    # Processar apenas inglês e espanhol (que têm duplicatas)
    for lang in ["en", "es"]:
        po_file = locale_dir / lang / "LC_MESSAGES" / "django.po"
        if po_file.exists():
            removed = fix_duplicates_in_file(po_file)
            total_removed += removed
    
    print(f"\n📊 Total de duplicatas removidas: {total_removed}")
    
    if total_removed > 0:
        print("✅ Execute: python manage.py compilemessages")
    
    return total_removed > 0

if __name__ == "__main__":
    main()

