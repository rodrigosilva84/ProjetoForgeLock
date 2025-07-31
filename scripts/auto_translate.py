#!/usr/bin/env python
"""
Script para tradução automática de strings não traduzidas.
Usa deep-translator para traduzir automaticamente.
"""

import os
import sys
import polib
import time
from pathlib import Path
from deep_translator import GoogleTranslator

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def auto_translate_po_file(po_file_path, target_lang):
    """Traduz automaticamente strings não traduzidas em um arquivo .po"""
    print(f"\nTraduzindo automaticamente: {po_file_path}")
    
    try:
        po = polib.pofile(po_file_path)
        
        # Mapeamento de idiomas
        lang_mapping = {
            'en': 'en',
            'es': 'es',
            'pt': 'pt'
        }
        
        target_lang_code = lang_mapping.get(target_lang, target_lang)
        translator = GoogleTranslator(source='pt', target=target_lang_code)
        translated_count = 0
        
        for entry in po:
            # Se a string não tem tradução
            if not entry.msgstr.strip():
                try:
                    # Traduzir automaticamente
                    translation = translator.translate(entry.msgid)
                    
                    # Salvar tradução
                    entry.msgstr = translation
                    translated_count += 1
                    
                    print(f"   OK: '{entry.msgid}' -> '{translation}'")
                    
                    # Pausa para não sobrecarregar a API
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"   ERROR: Erro ao traduzir '{entry.msgid}': {e}")
                    continue
        
        # Salvar arquivo traduzido
        po.save()
        
        print(f"   INFO: {translated_count} strings traduzidas automaticamente")
        return translated_count
        
    except Exception as e:
        print(f"ERROR: Erro ao processar {po_file_path}: {e}")
        return 0

def main():
    """Função principal"""
    print("Tradutor Automático - ForgeLock")
    print("=" * 50)
    
    locale_dir = Path("locale")
    if not locale_dir.exists():
        print("ERROR: Diretório 'locale' não encontrado!")
        return
    
    total_translated = 0
    files_processed = 0
    
    # Processar arquivos .po em todos os idiomas
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir() and lang_dir.name != 'pt':  # Pular português (original)
            po_file = lang_dir / "LC_MESSAGES" / "django.po"
            if po_file.exists():
                files_processed += 1
                total_translated += auto_translate_po_file(str(po_file), lang_dir.name)
    
    print("\n" + "=" * 50)
    print(f"Resumo:")
    print(f"   Arquivos processados: {files_processed}")
    print(f"   Total de strings traduzidas: {total_translated}")
    
    if total_translated > 0:
        print("\nPróximos passos:")
        print("   - Execute: python manage.py compilemessages")
        print("   - Teste as traduções no site")
        print("   - Revise traduções que precisam de ajuste")
    else:
        print("SUCCESS: Nenhuma string precisava de tradução!")

if __name__ == "__main__":
    main() 