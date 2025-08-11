#!/usr/bin/env python3
"""
Validador Inteligente de Traduções - ForgeLock
Previene erros automaticamente e organiza traduções por módulos
"""

import os
import re
import polib
from pathlib import Path
from collections import defaultdict, Counter

class SmartTranslationValidator:
    def __init__(self, locale_dir="locale"):
        self.locale_dir = Path(locale_dir)
        self.problems = []
        self.duplicates = []
        self.suggestions = []
        
    def analyze_po_file(self, po_file_path):
        """Analisa arquivo .po e detecta problemas"""
        try:
            po = polib.pofile(str(po_file_path))
            print(f"\n🔍 Analisando: {po_file_path.name}")
            
            # Detectar duplicatas
            msgids = [entry.msgid for entry in po if entry.msgid]
            duplicates = [msg for msg, count in Counter(msgids).items() if count > 1]
            
            if duplicates:
                self.duplicates.extend(duplicates)
                print(f"   ❌ {len(duplicates)} strings duplicadas encontradas")
            
            # Detectar strings muito longas
            long_strings = [entry for entry in po if len(entry.msgid) > 100]
            if long_strings:
                print(f"   ⚠️  {len(long_strings)} strings muito longas")
            
            # Detectar strings sem tradução
            untranslated = [entry for entry in po if not entry.msgstr and entry.msgid]
            if untranslated:
                print(f"   ⚠️  {len(untranslated)} strings sem tradução")
            
            return len(duplicates) == 0
            
        except Exception as e:
            print(f"   ❌ Erro ao analisar: {e}")
            return False
    
    def detect_template_issues(self):
        """Detecta problemas nos templates"""
        print("\n🔍 Analisando templates...")
        
        template_dir = Path("templates")
        translation_pattern = r'{%\s*translate\s+["\']([^"\']+)["\']\s*%}'
        
        all_strings = []
        string_locations = defaultdict(list)
        
        for template_file in template_dir.rglob("*.html"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(translation_pattern, content)
                    
                    for match in matches:
                        all_strings.append(match)
                        string_locations[match].append(str(template_file))
                        
            except Exception as e:
                print(f"   ❌ Erro ao ler {template_file}: {e}")
        
        # Detectar strings duplicadas nos templates
        duplicates = [s for s, count in Counter(all_strings).items() if count > 1]
        
        if duplicates:
            print(f"   ❌ {len(duplicates)} strings duplicadas nos templates:")
            for dup in duplicates[:5]:  # Mostrar apenas as primeiras 5
                locations = string_locations[dup]
                print(f"      '{dup}' aparece em: {', '.join(locations)}")
        
        return duplicates
    
    def suggest_standardized_keys(self):
        """Sugere chaves padronizadas para as strings"""
        print("\n💡 Sugestões de padronização:")
        
        # Mapear strings para chaves sugeridas
        suggestions = {
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
        
        for string, key in suggestions.items():
            print(f"   '{string}' → {key}")
    
    def create_clean_po_structure(self):
        """Cria estrutura limpa para arquivo .po"""
        print("\n🧹 Criando estrutura limpa...")
        
        # Estrutura organizada por módulos
        structure = {
            "common": {
                "search": "Pesquisar",
                "clear": "Limpar",
                "status": "Status",
                "active": "Ativo",
                "inactive": "Inativo",
                "name": "Nome",
                "code": "Código",
                "edit": "Editar",
                "delete": "Excluir",
                "save": "Salvar",
                "cancel": "Cancelar",
                "back": "Voltar",
                "confirm": "Confirmar",
                "actions": "Ações",
                "filters": "Filtros",
                "all": "Todos",
                "none": "Nenhum",
                "found": "Encontrado",
                "not_found": "Não encontrado"
            },
            "country": {
                "title": "Países",
                "new": "Novo País",
                "edit": "Editar País",
                "ddi": "DDI",
                "flag": "Bandeira",
                "search_placeholder": "Nome, código ou DDI..."
            },
            "category": {
                "title": "Categorias",
                "new": "Nova Categoria",
                "edit": "Editar Categoria",
                "description": "Descrição"
            },
            "scale": {
                "title": "Escalas",
                "new": "Nova Escala",
                "edit": "Editar Escala",
                "example": "Ex: 1:10, 1:100, etc."
            },
            "product_type": {
                "title": "Tipos de Produto",
                "new": "Novo Tipo",
                "edit": "Editar Tipo"
            }
        }
        
        return structure
    
    def validate_all(self):
        """Executa validação completa"""
        print("🚀 Validador Inteligente de Traduções - ForgeLock")
        print("=" * 60)
        
        success = True
        
        # Analisar arquivos .po
        for lang_dir in self.locale_dir.iterdir():
            if lang_dir.is_dir() and lang_dir.name != "__pycache__":
                po_file = lang_dir / "LC_MESSAGES" / "django.po"
                if po_file.exists():
                    if not self.analyze_po_file(po_file):
                        success = False
        
        # Detectar problemas nos templates
        template_duplicates = self.detect_template_issues()
        if template_duplicates:
            success = False
        
        # Sugerir melhorias
        self.suggest_standardized_keys()
        
        # Criar estrutura limpa
        clean_structure = self.create_clean_po_structure()
        
        print(f"\n📊 Resumo da Validação:")
        print(f"   ✅ Arquivos analisados: {len(list(self.locale_dir.iterdir())) - 1}")
        print(f"   ❌ Problemas encontrados: {len(self.duplicates) + len(template_duplicates)}")
        
        if success:
            print("   🎉 Validação passou com sucesso!")
        else:
            print("   ⚠️  Validação falhou - problemas encontrados")
        
        return success, clean_structure

def main():
    validator = SmartTranslationValidator()
    success, structure = validator.validate_all()
    
    if not success:
        print("\n🔧 Para corrigir automaticamente, execute:")
        print("   python scripts/fix_translations.py")
    
    return success

if __name__ == "__main__":
    main()

