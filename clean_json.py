#!/usr/bin/env python3
"""
Script para limpar caracteres especiais dos arquivos JSON
"""
import json
import unicodedata
import os

def remove_accents(text):
    """Remove acentos de um texto"""
    if isinstance(text, str):
        # Normaliza caracteres Unicode e remove acentos
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if not unicodedata.combining(c))
        return text
    return text

def clean_json_data(data):
    """Limpa dados JSON recursivamente"""
    if isinstance(data, dict):
        return {key: clean_json_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_json_data(item) for item in data]
    elif isinstance(data, str):
        return remove_accents(data)
    else:
        return data

def clean_json_file(input_file, output_file):
    """Limpa um arquivo JSON"""
    print(f"Limpando {input_file}...")
    
    # Lê o arquivo original
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Limpa os dados
    cleaned_data = clean_json_data(data)
    
    # Salva o arquivo limpo
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print(f"Arquivo limpo salvo em {output_file}")

if __name__ == "__main__":
    # Lista de arquivos para limpar
    files_to_clean = [
        "core_data.json",
        "products_data.json", 
        "customers_data.json"
    ]
    
    for file in files_to_clean:
        if os.path.exists(file):
            output_file = file.replace('.json', '_clean.json')
            clean_json_file(file, output_file)
        else:
            print(f"Arquivo {file} não encontrado")
    
    print("Limpeza concluída!")
