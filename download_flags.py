#!/usr/bin/env python3
"""
Script para baixar bandeiras faltantes dos países
"""

import os
import requests
import time
from pathlib import Path

def download_flags():
    """Baixa bandeiras faltantes para todos os países"""
    
    print("🚩 Iniciando download de bandeiras faltantes...")
    
    # Diretório das bandeiras
    flags_dir = Path("forgelock-web-platform/static/images/flags")
    flags_dir.mkdir(parents=True, exist_ok=True)
    
    # Lista completa de códigos de países (incluindo territórios especiais)
    country_codes = [
        # Países padrão ISO 3166-1 alpha-2
        'af', 'al', 'dz', 'ad', 'ao', 'ag', 'ar', 'am', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'be', 'bz', 'bj', 'bt', 'bo',
        'ba', 'bw', 'br', 'bn', 'bg', 'bf', 'bi', 'kh', 'cm', 'ca', 'cv', 'cf', 'td', 'cl', 'cn', 'co', 'km', 'cg', 'cd', 'ck', 'cr',
        'ci', 'hr', 'cu', 'cy', 'cz', 'dk', 'dj', 'dm', 'do', 'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'et', 'fj', 'fi', 'fr', 'ga', 'gm',
        'ge', 'de', 'gh', 'gr', 'gd', 'gt', 'gn', 'gw', 'gy', 'ht', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ir', 'iq', 'ie', 'il', 'it',
        'jm', 'jp', 'jo', 'kz', 'ke', 'ki', 'kp', 'kr', 'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', 'mo',
        'mk', 'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mr', 'mu', 'mx', 'fm', 'md', 'mc', 'mn', 'me', 'ma', 'mz', 'mm', 'na',
        'nr', 'np', 'nl', 'nz', 'ni', 'ne', 'ng', 'no', 'om', 'pk', 'pw', 'pa', 'pg', 'py', 'pe', 'ph', 'pl', 'pt', 'qa', 'ro',
        'ru', 'rw', 'kn', 'lc', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'rs', 'sc', 'sl', 'sg', 'sk', 'si', 'sb', 'so', 'za', 'es',
        'lk', 'sd', 'sr', 'sz', 'se', 'ch', 'sy', 'tw', 'tj', 'tz', 'th', 'tl', 'tg', 'to', 'tt', 'tn', 'tr', 'tm', 'ug', 'ua',
        'ae', 'gb', 'us', 'uy', 'uz', 'vu', 've', 'vn', 'ye', 'zm', 'zw',
        # Territórios especiais e dependências
        'ai', 'by', 'gl', 'gu', 'mp', 'vi', 'vg', 'ms', 'pr', 'ss', 'tv', 'va'
    ]
    
    # Verificar bandeiras existentes
    existing_flags = set()
    if flags_dir.exists():
        for file in flags_dir.glob("*.svg"):
            existing_flags.add(file.stem)
    
    print(f"📁 Bandeiras existentes: {len(existing_flags)}")
    
    # Países sem bandeiras
    missing_flags = [code for code in country_codes if code not in existing_flags]
    print(f"🌍 Bandeiras faltantes: {len(missing_flags)}")
    
    if not missing_flags:
        print("✅ Todas as bandeiras já estão presentes!")
        return
    
    # API para bandeiras (FlagCDN - oficial)
    base_url = "https://flagcdn.com/{}.svg"
    
    downloaded = 0
    failed = 0
    
    for code in missing_flags:
        flag_url = base_url.format(code)
        flag_path = flags_dir / f"{code}.svg"
        
        try:
            print(f"⬇️  Baixando {code.upper()}...")
            
            response = requests.get(flag_url, timeout=10)
            response.raise_for_status()
            
            with open(flag_path, 'wb') as f:
                f.write(response.content)
            
            downloaded += 1
            print(f"✅ {code.upper()} baixado com sucesso")
            
            # Pausa para não sobrecarregar a API
            time.sleep(0.5)
            
        except Exception as e:
            failed += 1
            print(f"❌ Erro ao baixar {code.upper()}: {str(e)}")
    
    print("")
    print(f"🎉 Download concluído! {downloaded} baixados, {failed} falharam")
    print(f"📊 Total de bandeiras no sistema: {len(existing_flags) + downloaded}")

if __name__ == "__main__":
    download_flags()
