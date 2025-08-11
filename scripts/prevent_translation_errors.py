#!/usr/bin/env python3
"""
Preventor de Erros de Tradução - ForgeLock
Previene problemas antes de acontecerem
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter

class TranslationErrorPreventor:
    def __init__(self):
        self.template_dir = Path("templates")
        self.locale_dir = Path("locale")
        self.errors = []
        self.warnings = []
        
    def check_template_consistency(self):
        """Verifica consistência dos templates"""
        print("🔍 Verificando consistência dos templates...")
        
        translation_pattern = r'{%\s*translate\s+["\']([^"\']+)["\']\s*%}'
        all_strings = []
        
        for template_file in self.template_dir.rglob("*.html"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(translation_pattern, content)
                    
                    for match in matches:
                        all_strings.append((match, template_file))
                        
            except Exception as e:
                self.errors.append(f"Erro ao ler {template_file}: {e}")
        
        # Verificar strings duplicadas
        string_count = Counter([s[0] for s in all_strings])
        duplicates = [s for s, count in string_count.items() if count > 1]
        
        if duplicates:
            self.warnings.append(f"Strings duplicadas encontradas: {len(duplicates)}")
            for dup in duplicates[:3]:  # Mostrar apenas as primeiras 3
                locations = [s[1] for s in all_strings if s[0] == dup]
                self.warnings.append(f"  '{dup}' aparece em: {', '.join(str(l) for l in locations[:3])}")
        
        return len(duplicates) == 0
    
    def check_po_file_integrity(self):
        """Verifica integridade dos arquivos .po"""
        print("🔍 Verificando integridade dos arquivos .po...")
        
        for lang_dir in self.locale_dir.iterdir():
            if lang_dir.is_dir() and lang_dir.name != "__pycache__":
                po_file = lang_dir / "LC_MESSAGES" / "django.po"
                if po_file.exists():
                    try:
                        with open(po_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Verificar BOM
                            if content.startswith('\ufeff'):
                                self.errors.append(f"BOM detectado em {po_file.name}")
                            
                            # Verificar linhas vazias problemáticas
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if line.strip() == '' and i < len(lines):
                                    next_line = lines[i].strip()
                                    if next_line.startswith('msgid') or next_line.startswith('msgstr'):
                                        self.warnings.append(f"Linha vazia problemática em {po_file.name}:{i}")
                            
                    except Exception as e:
                        self.errors.append(f"Erro ao verificar {po_file.name}: {e}")
        
        return len(self.errors) == 0
    
    def suggest_improvements(self):
        """Sugere melhorias para prevenir erros"""
        print("💡 Sugestões para prevenir erros:")
        
        suggestions = [
            "Use chaves padronizadas: {% translate 'common.search' %} em vez de {% translate 'Pesquisar' %}",
            "Agrupe traduções por módulo no arquivo .po",
            "Execute validação antes de cada commit",
            "Use CI/CD para verificar traduções automaticamente",
            "Mantenha um glossário de termos padronizados"
        ]
        
        for suggestion in suggestions:
            print(f"   • {suggestion}")
    
    def create_prevention_script(self):
        """Cria script de prevenção para CI/CD"""
        print("🔧 Criando script de prevenção...")
        
        script_content = '''#!/bin/bash
# Script de Prevenção de Erros de Tradução - ForgeLock

echo "🔍 Verificando traduções antes do commit..."

# Executar validação
python scripts/smart_translation_validator.py

if [ $? -eq 0 ]; then
    echo "✅ Traduções validadas com sucesso!"
    exit 0
else
    echo "❌ Problemas encontrados nas traduções!"
    echo "Execute: python scripts/fix_translations.py"
    exit 1
fi
'''
        
        with open("scripts/pre_commit_check.sh", "w") as f:
            f.write(script_content)
        
        print("   ✅ Script pre_commit_check.sh criado")
    
    def run_all_checks(self):
        """Executa todas as verificações"""
        print("🚀 Preventor de Erros de Tradução - ForgeLock")
        print("=" * 60)
        
        success = True
        
        # Verificar templates
        if not self.check_template_consistency():
            success = False
        
        # Verificar arquivos .po
        if not self.check_po_file_integrity():
            success = False
        
        # Mostrar resultados
        print(f"\n📊 Resultado das Verificações:")
        
        if self.errors:
            print(f"   ❌ Erros encontrados: {len(self.errors)}")
            for error in self.errors[:5]:  # Mostrar apenas os primeiros 5
                print(f"      • {error}")
        
        if self.warnings:
            print(f"   ⚠️  Avisos: {len(self.warnings)}")
            for warning in self.warnings[:5]:  # Mostrar apenas os primeiros 5
                print(f"      • {warning}")
        
        if not self.errors and not self.warnings:
            print("   ✅ Nenhum problema encontrado!")
        
        # Sugerir melhorias
        self.suggest_improvements()
        
        # Criar script de prevenção
        self.create_prevention_script()
        
        print(f"\n🔧 Para corrigir problemas automaticamente:")
        print("   python scripts/fix_translations.py")
        
        print(f"\n🔧 Para validação completa:")
        print("   python scripts/smart_translation_validator.py")
        
        return success

def main():
    preventor = TranslationErrorPreventor()
    return preventor.run_all_checks()

if __name__ == "__main__":
    main()

