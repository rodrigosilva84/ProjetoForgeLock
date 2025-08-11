#!/usr/bin/env python3
"""
Corretor de Headers Duplicados - ForgeLock
Corrige o problema específico dos headers msgid "" duplicados
"""

import re
from pathlib import Path

def fix_header_duplicates(po_file_path):
    """Corrige duplicatas de headers em arquivo .po"""
    try:
        print(f"🔍 Processando: {po_file_path.name}")
        
        # Ler arquivo
        with open(po_file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Padrão para encontrar headers duplicados
        # Procurar por múltiplas ocorrências de msgid "" vazias
        header_pattern = r'(msgid ""\s+msgstr ""\s+".*?"\s*)+'
        
        # Encontrar todos os headers
        headers = re.findall(header_pattern, content, re.DOTALL)
        
        if len(headers) > 1:
            print(f"   🗑️  {len(headers)} headers encontrados")
            
            # Manter apenas o primeiro header e remover os outros
            first_header = headers[0]
            other_headers = headers[1:]
            
            for header in other_headers:
                content = content.replace(header, '')
            
            # Salvar arquivo corrigido
            with open(po_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ Headers duplicados removidos")
            return len(other_headers)
        else:
            print(f"   ✅ Nenhum header duplicado encontrado")
            return 0
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return 0

def main():
    print("🔧 Corretor de Headers Duplicados - ForgeLock")
    print("=" * 55)
    
    locale_dir = Path("locale")
    total_fixed = 0
    
    # Processar inglês e espanhol
    for lang in ["en", "es"]:
        po_file = locale_dir / lang / "LC_MESSAGES" / "django.po"
        if po_file.exists():
            fixed = fix_header_duplicates(po_file)
            total_fixed += fixed
    
    print(f"\n📊 Total de headers corrigidos: {total_fixed}")
    
    if total_fixed > 0:
        print("✅ Execute: python manage.py compilemessages")
    
    return total_fixed > 0

if __name__ == "__main__":
    main()

