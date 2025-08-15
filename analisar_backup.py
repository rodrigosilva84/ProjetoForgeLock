#!/usr/bin/env python
import json
from datetime import datetime

def analisar_backup():
    """Analisa o backup do banco de dados"""
    try:
        # Ler o arquivo com encoding UTF-8
        with open('backup_completo_20250814_234736.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("=" * 60)
        print("📊 ANÁLISE DO BACKUP COMPLETO")
        print("=" * 60)
        
        # Contar tabelas e registros
        total_tables = len(data)
        total_records = 0
        
        print(f"\n📋 TOTAL DE TABELAS: {total_tables}")
        print("-" * 40)
        
        # Listar tabelas com contagem de registros
        for table_name, records in data.items():
            record_count = len(records) if records else 0
            total_records += record_count
            
            # Identificar tabelas importantes
            if table_name in ['auth_user', 'company_company', 'products_product', 'customers_customer']:
                print(f"🔴 {table_name:<25} : {record_count:>3} registros")
            elif 'migration' in table_name:
                print(f"🟡 {table_name:<25} : {record_count:>3} registros")
            else:
                print(f"⚪ {table_name:<25} : {record_count:>3} registros")
        
        print("-" * 40)
        print(f"📈 TOTAL DE REGISTROS: {total_records}")
        
        # Análise detalhada das tabelas importantes
        print("\n" + "=" * 60)
        print("🔍 ANÁLISE DETALHADA DAS TABELAS PRINCIPAIS")
        print("=" * 60)
        
        # Usuários
        if 'auth_user' in data:
            users = data['auth_user']
            print(f"\n👥 USUÁRIOS ({len(users)} registros):")
            for user in users:
                username = user.get('username', 'N/A')
                email = user.get('email', 'N/A')
                is_active = user.get('is_active', False)
                status = "✅ Ativo" if is_active else "❌ Inativo"
                print(f"  - {username:<15} | {email:<25} | {status}")
        
        # Empresas
        if 'company_company' in data:
            companies = data['company_company']
            print(f"\n🏢 EMPRESAS ({len(companies)} registros):")
            for company in companies:
                name = company.get('name', 'N/A')
                is_active = company.get('is_active', False)
                status = "✅ Ativa" if is_active else "❌ Inativa"
                print(f"  - {name:<20} | {status}")
        
        # Produtos
        if 'products_product' in data:
            products = data['products_product']
            print(f"\n📦 PRODUTOS ({len(products)} registros):")
            for product in products:
                name = product.get('name', 'N/A')
                is_active = product.get('is_active', False)
                status = "✅ Ativo" if is_active else "❌ Inativo"
                print(f"  - {name:<25} | {status}")
        
        # Clientes
        if 'customers_customer' in data:
            customers = data['customers_customer']
            print(f"\n👤 CLIENTES ({len(customers)} registros):")
            for customer in customers:
                name = customer.get('name', 'N/A')
                is_active = customer.get('is_active', False)
                status = "✅ Ativo" if is_active else "❌ Inativo"
                print(f"  - {name:<25} | {status}")
        
        print("\n" + "=" * 60)
        print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao analisar backup: {e}")
        return False

if __name__ == '__main__':
    analisar_backup()

