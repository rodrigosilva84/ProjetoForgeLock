#!/usr/bin/env python3
"""
Script para restaurar dados do backup SQLite para PostgreSQL
"""
import json
import os
import django
from django.conf import settings
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forgelock.settings')
django.setup()

def restore_data_from_backup():
    """Restaura dados do backup para o banco PostgreSQL"""
    
    backup_file = 'backup_completo_20250814_234736.json'
    
    if not os.path.exists(backup_file):
        print(f"❌ Arquivo de backup não encontrado: {backup_file}")
        return False
    
    try:
        print("📖 Carregando backup...")
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        print(f"✅ Backup carregado: {len(backup_data)} tabelas")
        
        # Ordem de restauração (respeitando dependências)
        restore_order = [
            'django_content_type',
            'auth_permission', 
            'core_country',
            'core_plan',
            'core_planprice',
            'core_user',
            'core_company',
            'core_usercompany',
            'core_account',
            'core_subscription',
            'products_currency',
            'products_scale',
            'products_category',
            'products_producttype',
            'products_product',
            'products_productimage',
            'customers_customer',
            'django_admin_log',
            'django_session'
        ]
        
        total_restored = 0
        
        for table_name in restore_order:
            if table_name in backup_data:
                table_data = backup_data[table_name]
                if table_data:
                    print(f"🔄 Restaurando {table_name}: {len(table_data)} registros...")
                    
                    try:
                        # Restaurar dados da tabela
                        restored_count = restore_table_data(table_name, table_data)
                        total_restored += restored_count
                        print(f"✅ {table_name}: {restored_count} registros restaurados")
                        
                    except Exception as e:
                        print(f"❌ Erro ao restaurar {table_name}: {e}")
                        continue
                else:
                    print(f"⚪ {table_name}: Sem dados para restaurar")
            else:
                print(f"⚠️ {table_name}: Tabela não encontrada no backup")
        
        print(f"\n🎉 RESTAURAÇÃO CONCLUÍDA!")
        print(f"📊 Total de registros restaurados: {total_restored}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao restaurar backup: {e}")
        return False

def restore_table_data(table_name, table_data):
    """Restaura dados de uma tabela específica"""
    
    if not table_data:
        return 0
    
    # Mapear nomes de tabelas para modelos Django
    model_mapping = {
        'core_country': 'core.Country',
        'core_plan': 'core.Plan',
        'core_planprice': 'core.PlanPrice',
        'core_user': 'core.User',
        'core_company': 'core.Company',
        'core_usercompany': 'core.UserCompany',
        'core_account': 'core.Account',
        'core_subscription': 'core.Subscription',
        'products_currency': 'products.Currency',
        'products_scale': 'products.Scale',
        'products_category': 'products.Category',
        'products_producttype': 'products.ProductType',
        'products_product': 'products.Product',
        'products_productimage': 'products.ProductImage',
        'customers_customer': 'customers.Customer'
    }
    
    if table_name not in model_mapping:
        print(f"⚠️ Modelo não mapeado para {table_name}")
        return 0
    
    try:
        # Importar o modelo
        app_label, model_name = model_mapping[table_name].split('.')
        model = django.apps.apps.get_model(app_label, model_name)
        
        restored_count = 0
        
        for record in table_data:
            try:
                # Remover campos que não existem no modelo atual
                cleaned_record = clean_record_for_model(record, model)
                
                # Criar ou atualizar o registro
                obj, created = model.objects.update_or_create(
                    id=cleaned_record.get('id'),
                    defaults=cleaned_record
                )
                
                if created:
                    restored_count += 1
                else:
                    restored_count += 1
                    
            except Exception as e:
                print(f"⚠️ Erro ao restaurar registro em {table_name}: {e}")
                continue
        
        return restored_count
        
    except Exception as e:
        print(f"❌ Erro ao restaurar tabela {table_name}: {e}")
        return 0

def clean_record_for_model(record, model):
    """Remove campos que não existem no modelo atual"""
    cleaned = {}
    
    for field_name, value in record.items():
        if hasattr(model, field_name):
            # Converter tipos de dados se necessário
            field = model._meta.get_field(field_name)
            
            if field.get_internal_type() == 'BooleanField':
                cleaned[field_name] = bool(value) if value is not None else False
            elif field.get_internal_type() == 'DecimalField':
                if value is not None and value != '':
                    try:
                        cleaned[field_name] = float(value)
                    except (ValueError, TypeError):
                        cleaned[field_name] = None
                else:
                    cleaned[field_name] = None
            else:
                cleaned[field_name] = value
    
    return cleaned

if __name__ == '__main__':
    print("🚀 INICIANDO RESTAURAÇÃO DO BACKUP PARA POSTGRESQL")
    print("=" * 60)
    
    success = restore_data_from_backup()
    
    if success:
        print("\n✅ Restauração concluída com sucesso!")
        print("🌐 Acesse: http://127.0.0.1:8000/")
        print("🔐 Admin: http://127.0.0.1:8000/admin/")
    else:
        print("\n❌ Restauração falhou!")
