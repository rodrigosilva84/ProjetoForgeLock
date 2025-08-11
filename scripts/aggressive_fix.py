#!/usr/bin/env python3
"""
Corretor Agressivo de Traduções - ForgeLock
Remove TODAS as duplicatas e problemas
"""

import os
import shutil
import polib
from pathlib import Path
from collections import defaultdict

class AggressiveTranslationFixer:
    def __init__(self, locale_dir="locale"):
        self.locale_dir = Path(locale_dir)
        self.backup_dir = Path("locale_backup_aggressive")
        
    def create_backup(self):
        """Cria backup dos arquivos de tradução"""
        print("💾 Criando backup agressivo...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        shutil.copytree(self.locale_dir, self.backup_dir)
        print("   ✅ Backup criado em locale_backup_aggressive/")
    
    def aggressive_cleanup(self, po_file_path):
        """Limpeza agressiva do arquivo .po"""
        try:
            print(f"   🔥 Limpeza agressiva em {po_file_path.name}")
            
            # Ler arquivo linha por linha
            with open(po_file_path, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
            
            # Remover BOM se existir
            if lines and lines[0].startswith('\ufeff'):
                lines[0] = lines[0].lstrip('\ufeff')
            
            # Processar e remover duplicatas
            cleaned_lines = []
            seen_msgids = set()
            in_entry = False
            current_entry = []
            entry_count = 0
            
            for line in lines:
                if line.startswith('msgid '):
                    # Novo entry
                    if current_entry and in_entry:
                        # Processar entry anterior
                        msgid = self.extract_msgid(current_entry)
                        if msgid and msgid not in seen_msgids:
                            seen_msgids.add(msgid)
                            cleaned_lines.extend(current_entry)
                            entry_count += 1
                        elif msgid:
                            print(f"      🗑️  Duplicata removida: '{msgid[:50]}...'")
                    
                    # Iniciar novo entry
                    current_entry = [line]
                    in_entry = True
                    
                elif line.startswith('msgstr ') and in_entry:
                    # Continuar entry
                    current_entry.append(line)
                    
                elif line.strip() == '' and in_entry:
                    # Fim do entry
                    current_entry.append(line)
                    in_entry = False
                    
                elif in_entry:
                    # Continuar entry
                    current_entry.append(line)
                    
                else:
                    # Linha de comentário ou metadados
                    cleaned_lines.append(line)
            
            # Processar último entry
            if current_entry and in_entry:
                msgid = self.extract_msgid(current_entry)
                if msgid and msgid not in seen_msgids:
                    seen_msgids.add(msgid)
                    cleaned_lines.extend(current_entry)
                    entry_count += 1
            
            # Salvar arquivo limpo
            with open(po_file_path, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)
            
            print(f"      ✅ {entry_count} entradas únicas mantidas")
            return entry_count
            
        except Exception as e:
            print(f"      ❌ Erro: {e}")
            return 0
    
    def extract_msgid(self, entry_lines):
        """Extrai msgid de um conjunto de linhas"""
        for line in entry_lines:
            if line.startswith('msgid '):
                return line[6:].strip().strip('"')
        return None
    
    def fix_headers(self, po_file_path):
        """Corrige headers dos arquivos .po"""
        try:
            po = polib.pofile(str(po_file_path))
            
            # Corrigir headers
            if 'charset' not in po.metadata:
                po.metadata['charset'] = 'utf-8'
            
            if 'Content-Type' not in po.metadata:
                po.metadata['Content-Type'] = 'text/plain; charset=utf-8'
            
            po.save(str(po_file_path))
            print(f"      🔧 Headers corrigidos")
            
        except Exception as e:
            print(f"      ❌ Erro ao corrigir headers: {e}")
    
    def fix_all_files(self):
        """Corrige todos os arquivos de tradução"""
        print("🔥 Corretor Agressivo de Traduções - ForgeLock")
        print("=" * 60)
        
        # Criar backup
        self.create_backup()
        
        total_entries = 0
        
        # Processar cada arquivo .po
        for lang_dir in self.locale_dir.iterdir():
            if lang_dir.is_dir() and lang_dir.name != "__pycache__":
                po_file = lang_dir / "LC_MESSAGES" / "django.po"
                if po_file.exists():
                    print(f"\n🔍 Processando: {po_file.name}")
                    
                    # Limpeza agressiva
                    entries = self.aggressive_cleanup(po_file)
                    total_entries += entries
                    
                    # Corrigir headers
                    self.fix_headers(po_file)
        
        print(f"\n📊 Resumo da Limpeza Agressiva:")
        print(f"   🔥 Entradas únicas mantidas: {total_entries}")
        print(f"   💾 Backup criado em: locale_backup_aggressive/")
        
        print(f"\n✅ Limpeza agressiva concluída!")
        print(f"   Execute: python manage.py compilemessages")
        
        return True

def main():
    fixer = AggressiveTranslationFixer()
    return fixer.fix_all_files()

if __name__ == "__main__":
    main()

