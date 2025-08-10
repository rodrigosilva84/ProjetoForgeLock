#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

def create_clean_svg(flag_code, colors):
    """Cria um arquivo SVG limpo para a bandeira"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3 2">
{colors}
</svg>'''
    return svg_content

def fix_all_flags():
    """Corrige todos os arquivos SVG corrompidos"""
    flags_dir = os.path.join('static', 'images', 'flags')
    
    # Definições das bandeiras (código: cores SVG)
    flag_definitions = {
        'it': '''  <rect width="1" height="2" x="0" y="0" fill="green"/>
  <rect width="1" height="2" x="1" y="0" fill="white"/>
  <rect width="1" height="2" x="2" y="0" fill="red"/>''',
        
        'mx': '''  <rect width="3" height="2" x="0" y="0" fill="green"/>
  <rect width="3" height="1" x="0" y="0.5" fill="white"/>
  <rect width="3" height="0.5" x="0" y="1" fill="red"/>
  <circle cx="1.5" cy="1" r="0.3" fill="#006847"/>
  <circle cx="1.5" cy="1" r="0.25" fill="white"/>
  <circle cx="1.5" cy="1" r="0.2" fill="#006847"/>
  <circle cx="1.5" cy="1" r="0.15" fill="white"/>
  <circle cx="1.5" cy="1" r="0.1" fill="#006847"/>''',
        
        'pe': '''  <rect width="3" height="2" x="0" y="0" fill="#D91023"/>
  <rect width="1" height="2" x="1" y="0" fill="white"/>''',
        
        'pt': '''  <rect width="3" height="2" x="0" y="0" fill="green"/>
  <rect width="1" height="2" x="2" y="0" fill="red"/>
  <circle cx="1.5" cy="1" r="0.4" fill="#FFD900"/>
  <circle cx="1.5" cy="1" r="0.35" fill="#006600"/>
  <circle cx="1.5" cy="1" r="0.25" fill="#FFD900"/>
  <circle cx="1.5" cy="1" r="0.2" fill="#006600"/>
  <circle cx="1.5" cy="1" r="0.1" fill="#FFD900"/>''',
        
        'uy': '''  <rect width="3" height="2" x="0" y="0" fill="white"/>
  <rect width="3" height="0.25" x="0" y="0.25" fill="#0038A8"/>
  <rect width="3" height="0.25" x="0" y="0.75" fill="#0038A8"/>
  <rect width="3" height="0.25" x="0" y="1.25" fill="#0038A8"/>
  <rect width="3" height="0.25" x="0" y="1.75" fill="#0038A8"/>
  <rect width="1" height="2" x="0" y="0" fill="#FFD900"/>
  <circle cx="0.5" cy="1" r="0.15" fill="white"/>
  <circle cx="0.5" cy="1" r="0.1" fill="#0038A8"/>''',
        
        've': '''  <rect width="3" height="2" x="0" y="0" fill="#FFD900"/>
  <rect width="3" height="0.67" x="0" y="0.67" fill="#0038A8"/>
  <rect width="3" height="0.67" x="0" y="1.33" fill="#CE1126"/>
  <circle cx="1.5" cy="1" r="0.2" fill="white"/>
  <circle cx="1.5" cy="1" r="0.15" fill="#0038A8"/>'''
    }
    
    print("=== CORRIGINDO TODAS AS BANDEIRAS ===")
    
    for flag_code, colors in flag_definitions.items():
        flag_path = os.path.join(flags_dir, f'{flag_code}.svg')
        
        if os.path.exists(flag_path):
            # Criar conteúdo SVG limpo
            clean_svg = create_clean_svg(flag_code, colors)
            
            # Salvar arquivo
            with open(flag_path, 'w', encoding='utf-8') as f:
                f.write(clean_svg)
            
            print(f"✅ {flag_code.upper()} - Bandeira corrigida")
        else:
            print(f"⚠️  {flag_code.upper()} - Arquivo não encontrado")
    
    print("\n=== VERIFICAÇÃO FINAL ===")
    for flag_code in flag_definitions.keys():
        flag_path = os.path.join(flags_dir, f'{flag_code}.svg')
        if os.path.exists(flag_path):
            with open(flag_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('<?xml') and 'svg' in content:
                    print(f"✅ {flag_code.upper()} - Arquivo válido")
                else:
                    print(f"❌ {flag_code.upper()} - Arquivo ainda corrompido")
        else:
            print(f"❌ {flag_code.upper()} - Arquivo não existe")

if __name__ == "__main__":
    fix_all_flags()
