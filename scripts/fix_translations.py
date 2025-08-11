#!/usr/bin/env python3
"""
Corretor Automático de Traduções - ForgeLock
Corrige problemas automaticamente e organiza traduções
"""

import os
import shutil
import polib
from pathlib import Path
from collections import defaultdict

class TranslationFixer:
    def __init__(self, locale_dir="locale"):
        self.locale_dir = Path(locale_dir)
        self.backup_dir = Path("locale_backup")
        
    def create_backup(self):
        """Cria backup dos arquivos de tradução"""
        print("💾 Criando backup...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        shutil.copytree(self.locale_dir, self.backup_dir)
        print("   ✅ Backup criado em locale_backup/")
    
    def remove_duplicates(self, po_file_path):
        """Remove strings duplicadas do arquivo .po"""
        try:
            po = polib.pofile(str(po_file_path))
            
            # Contar ocorrências de cada msgid
            msgid_count = defaultdict(int)
            for entry in po:
                if entry.msgid:
                    msgid_count[entry.msgid] += 1
            
            # Remover duplicatas, mantendo apenas a primeira
            seen_msgids = set()
            entries_to_remove = []
            
            for i, entry in enumerate(po):
                if entry.msgid and entry.msgid in seen_msgids:
                    entries_to_remove.append(i)
                elif entry.msgid:
                    seen_msgids.add(entry.msgid)
            
            # Remover entradas duplicadas (em ordem reversa para não afetar índices)
            for i in reversed(entries_to_remove):
                po.remove(po[i])
            
            # Salvar arquivo limpo
            po.save(str(po_file_path))
            
            removed_count = len(entries_to_remove)
            if removed_count > 0:
                print(f"   🧹 Removidas {removed_count} strings duplicadas")
            
            return removed_count
            
        except Exception as e:
            print(f"   ❌ Erro ao processar {po_file_path.name}: {e}")
            return 0
    
    def standardize_keys(self, po_file_path):
        """Padroniza chaves de tradução"""
        try:
            po = polib.pofile(str(po_file_path))
            
            # Mapeamento de strings para chaves padronizadas
            key_mapping = {
                "Pesquisar": "common.search",
                "Limpar": "common.clear",
                "Status": "common.status",
                "Ativo": "common.active",
                "Inativo": "common.inactive",
                "Nome": "common.name",
                "Código": "common.code",
                "Editar": "common.edit",
                "Excluir": "common.delete",
                "Salvar": "common.save",
                "Cancelar": "common.cancel",
                "Voltar": "common.back",
                "Confirmar": "common.confirm",
                "Ações": "common.actions",
                "Filtros": "common.filters",
                "Todos": "common.all",
                "Nenhum": "common.none",
                "Encontrado": "common.found",
                "Não encontrado": "common.not_found"
            }
            
            # Aplicar mapeamento
            changes = 0
            for entry in po:
                if entry.msgid in key_mapping:
                    old_msgid = entry.msgid
                    entry.msgid = key_mapping[entry.msgid]
                    changes += 1
                    print(f"      '{old_msgid}' → '{entry.msgid}'")
            
            if changes > 0:
                po.save(str(po_file_path))
                print(f"   🔄 {changes} chaves padronizadas")
            
            return changes
            
        except Exception as e:
            print(f"   ❌ Erro ao padronizar {po_file_path.name}: {e}")
            return 0
    
    def fix_encoding(self, po_file_path):
        """Corrige problemas de codificação"""
        try:
            # Ler arquivo com detecção automática de encoding
            with open(po_file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # Remover BOM e salvar em UTF-8 puro
            with open(po_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   🔧 Codificação corrigida")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao corrigir codificação: {e}")
            return False
    
    def organize_by_modules(self, po_file_path):
        """Organiza traduções por módulos"""
        try:
            po = polib.pofile(str(po_file_path))
            
            # Agrupar entradas por módulo
            modules = defaultdict(list)
            
            for entry in po:
                if entry.msgid:
                    # Determinar módulo baseado no contexto
                    module = "common"
                    if "country" in str(entry.occurrences):
                        module = "country"
                    elif "category" in str(entry.occurrences):
                        module = "category"
                    elif "scale" in str(entry.occurrences):
                        module = "scale"
                    elif "product_type" in str(entry.occurrences):
                        module = "product_type"
                    elif "product" in str(entry.occurrences):
                        module = "product"
                    elif "customer" in str(entry.occurrences):
                        module = "customer"
                    
                    modules[module].append(entry)
            
            # Reorganizar arquivo por módulos
            new_po = polib.POFile()
            new_po.metadata = po.metadata
            
            # Adicionar comentários de separação por módulo
            for module, entries in modules.items():
                if entries:
                    # Adicionar comentário de separação
                    separator = polib.POEntry()
                    separator.comment = f"=== {module.upper()} ==="
                    new_po.append(separator)
                    
                    # Adicionar entradas do módulo
                    for entry in entries:
                        new_po.append(entry)
            
            # Salvar arquivo reorganizado
            new_po.save(str(po_file_path))
            
            print(f"   📁 Organizado em {len(modules)} módulos")
            return len(modules)
            
        except Exception as e:
            print(f"   ❌ Erro ao organizar módulos: {e}")
            return 0
    
    def fix_all_files(self):
        """Corrige todos os arquivos de tradução"""
        print("🔧 Corretor Automático de Traduções - ForgeLock")
        print("=" * 60)
        
        # Criar backup
        self.create_backup()
        
        total_duplicates = 0
        total_standardized = 0
        total_modules = 0
        
        # Processar cada arquivo .po
        for lang_dir in self.locale_dir.iterdir():
            if lang_dir.is_dir() and lang_dir.name != "__pycache__":
                po_file = lang_dir / "LC_MESSAGES" / "django.po"
                if po_file.exists():
                    print(f"\n🔍 Processando: {po_file.name}")
                    
                    # Corrigir codificação
                    self.fix_encoding(po_file)
                    
                    # Remover duplicatas
                    duplicates = self.remove_duplicates(po_file)
                    total_duplicates += duplicates
                    
                    # Padronizar chaves
                    standardized = self.standardize_keys(po_file)
                    total_standardized += standardized
                    
                    # Organizar por módulos
                    modules = self.organize_by_modules(po_file)
                    total_modules += modules
        
        print(f"\n📊 Resumo das Correções:")
        print(f"   🧹 Strings duplicadas removidas: {total_duplicates}")
        print(f"   🔄 Chaves padronizadas: {total_standardized}")
        print(f"   📁 Módulos organizados: {total_modules}")
        print(f"   💾 Backup criado em: locale_backup/")
        
        print(f"\n✅ Correções concluídas!")
        print(f"   Execute: python manage.py compilemessages")
        
        return True

def main():
    fixer = TranslationFixer()
    return fixer.fix_all_files()

if __name__ == "__main__":
    main()

