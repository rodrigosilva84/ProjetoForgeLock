#!/usr/bin/env python
import sqlite3
import json
from datetime import datetime

def backup_database():
    """Faz backup completo do banco SQLite"""
    try:
        # Conectar ao banco
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Obter lista de tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        backup_data = {}
        print(f"Fazendo backup de {len(tables)} tabelas...")
        
        for table in tables:
            table_name = table[0]
            print(f"  - Backup da tabela: {table_name}")
            
            try:
                # Obter dados da tabela
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if rows:
                    # Obter nomes das colunas
                    columns = [description[0] for description in cursor.description]
                    
                    # Converter para lista de dicionários
                    table_data = []
                    for row in rows:
                        row_dict = {}
                        for i, value in enumerate(row):
                            # Converter tipos não serializáveis
                            if isinstance(value, bytes):
                                value = value.hex()
                            row_dict[columns[i]] = value
                        table_data.append(row_dict)
                    
                    backup_data[table_name] = table_data
                    print(f"    ✓ {len(rows)} registros salvos")
                else:
                    backup_data[table_name] = []
                    print(f"    ✓ Tabela vazia")
                    
            except Exception as e:
                print(f"    ❌ Erro na tabela {table_name}: {e}")
                backup_data[table_name] = []
        
        conn.close()
        
        # Salvar backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_completo_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Backup completo salvo em: {filename}")
        print(f"📊 Total de tabelas: {len(tables)}")
        
        # Estatísticas
        total_records = sum(len(data) for data in backup_data.values())
        print(f"📈 Total de registros: {total_records}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Erro durante backup: {e}")
        return None

if __name__ == '__main__':
    backup_database()

