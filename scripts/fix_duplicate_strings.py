#!/usr/bin/env python3
"""
Corretor de Strings Duplicadas - ForgeLock
Remove strings duplicadas específicas que causam problemas de compilação
"""
import re
from pathlib import Path

def fix_duplicate_strings(po_file_path):
    """Corrige strings duplicadas específicas"""
    try:
        print(f"🔍 Processando: {po_file_path.name}")
        
        # Ler arquivo
        with open(po_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Padrões de strings duplicadas problemáticas
        duplicates_to_fix = [
            'Status',
            'Pesquisar',
            'Limpar',
            'Nome',
            'Código',
            'Editar',
            'Ativo',
            'Inativo',
            'Todos',
            'Ações'
        ]
        
        total_fixed = 0
        
        for string in duplicates_to_fix:
            # Encontrar todas as ocorrências da string
            pattern = rf'^#: .*\.html:\d+\nmsgid "{re.escape(string)}"\nmsgstr ""\n'
            matches = list(re.finditer(pattern, content, re.MULTILINE))
            
            if len(matches) > 1:
                print(f"   🗑️  {len(matches)} duplicatas de '{string}' encontradas")
                
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
                
                total_fixed += len(other_matches)
                print(f"   ✅ {len(other_matches)} duplicatas de '{string}' removidas")
        
        if total_fixed > 0:
            # Salvar arquivo corrigido
            with open(po_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   💾 Arquivo salvo com {total_fixed} correções")
        
        return total_fixed
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return 0

def main():
    print("🔧 Corretor de Strings Duplicadas - ForgeLock")
    print("=" * 50)
    
    locale_dir = Path("locale")
    total_fixed = 0
    
    # Processar português (que tem problemas)
    po_file = locale_dir / "pt" / "LC_MESSAGES" / "django.po"
    if po_file.exists():
        fixed = fix_duplicate_strings(po_file)
        total_fixed += fixed
    
    print(f"\n📊 Total de strings corrigidas: {total_fixed}")
    
    if total_fixed > 0:
        print("✅ Execute: python manage.py compilemessages")
    
    return total_fixed > 0

if __name__ == "__main__":
    main()

