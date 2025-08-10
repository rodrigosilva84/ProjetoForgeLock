#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

def check_all_flags():
    """Verifica todas as bandeiras e identifica problemas"""
    flags_dir = os.path.join('static', 'images', 'flags')
    
    print("=== VERIFICAÇÃO COMPLETA DE TODAS AS BANDEIRAS ===")
    
    # Listar todos os arquivos SVG
    if os.path.exists(flags_dir):
        svg_files = [f for f in os.listdir(flags_dir) if f.endswith('.svg')]
        svg_files.sort()
        
        print(f"\nTotal de arquivos SVG encontrados: {len(svg_files)}")
        
        corrupted_files = []
        valid_files = []
        
        for svg_file in svg_files:
            flag_path = os.path.join(flags_dir, svg_file)
            
            try:
                with open(flag_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Verificar se o arquivo é válido
                if content.startswith('<?xml') and 'svg' in content and '<svg' in content:
                    valid_files.append(svg_file)
                    print(f"✅ {svg_file} - VÁLIDO")
                else:
                    corrupted_files.append(svg_file)
                    print(f"❌ {svg_file} - CORROMPIDO")
                    
                    # Mostrar primeiras linhas para diagnóstico
                    first_lines = content.split('\n')[:3]
                    print(f"   Primeiras linhas: {first_lines}")
                    
            except Exception as e:
                corrupted_files.append(svg_file)
                print(f"❌ {svg_file} - ERRO AO LER: {e}")
        
        print(f"\n=== RESUMO ===")
        print(f"✅ Arquivos válidos: {len(valid_files)}")
        print(f"❌ Arquivos corrompidos: {len(corrupted_files)}")
        
        if corrupted_files:
            print(f"\n📋 Arquivos que precisam ser corrigidos:")
            for file in corrupted_files:
                print(f"   - {file}")
        else:
            print(f"\n🎉 Todas as bandeiras estão funcionando perfeitamente!")
            
    else:
        print("❌ Diretório de bandeiras não encontrado!")

if __name__ == "__main__":
    check_all_flags()
