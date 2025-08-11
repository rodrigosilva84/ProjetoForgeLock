#!/usr/bin/env python3
"""
Corretor de msgid Vazios - ForgeLock
Remove todas as entradas msgid "" vazias exceto a primeira
"""

import re
from pathlib import Path

def fix_empty_msgids(po_file_path):
    """Corrige entradas msgid "" vazias duplicadas"""
    try:
        print(f"🔍 Processando: {po_file_path.name}")
        
        # Ler arquivo
        with open(po_file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Padrão para encontrar entradas msgid "" vazias
        # Procurar por linhas que começam com msgid "" e têm msgstr "" vazio
        empty_pattern = r'^msgid ""\s*^msgstr ""\s*^'
        
        # Encontrar todas as ocorrências
        matches = list(re.finditer(empty_pattern, content, re.MULTILINE | re.DOTALL))
        
        if len(matches) > 1:
            print(f"   🗑️  {len(matches)} entradas msgid vazias encontradas")
            
            # Manter apenas a primeira e remover as outras
            first_match = matches[0]
            other_matches = matches[1:]
            
            # Remover as outras entradas (em ordem reversa para não afetar índices)
            for match in reversed(other_matches):
                # Encontrar o final da entrada (próxima linha não vazia ou fim do arquivo)
                start_pos = match.start()
                end_pos = content.find('\n\n', start_pos)
                if end_pos == -1:
                    end_pos = len(content)
                else:
                    end_pos += 2  # Incluir as duas quebras de linha
                
                # Remover a entrada
                content = content[:start_pos] + content[end_pos:]
            
            # Salvar arquivo corrigido
            with open(po_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ {len(other_matches)} entradas msgid vazias removidas")
            return len(other_matches)
        else:
            print(f"   ✅ Nenhuma entrada msgid vazia duplicada encontrada")
            return 0
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return 0

def main():
    print("🔧 Corretor de msgid Vazios - ForgeLock")
    print("=" * 50)
    
    locale_dir = Path("locale")
    total_fixed = 0
    
    # Processar inglês e espanhol
    for lang in ["en", "es"]:
        po_file = locale_dir / lang / "LC_MESSAGES" / "django.po"
        if po_file.exists():
            fixed = fix_empty_msgids(po_file)
            total_fixed += fixed
    
    print(f"\n📊 Total de entradas corrigidas: {total_fixed}")
    
    if total_fixed > 0:
        print("✅ Execute: python manage.py compilemessages")
    
    return total_fixed > 0

if __name__ == "__main__":
    main()

