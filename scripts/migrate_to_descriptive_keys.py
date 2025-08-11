#!/usr/bin/env python3
"""
Migração para Chaves Descritivas - ForgeLock
Converte todas as traduções para sistema de chaves organizadas por módulos
"""
import re
import os
from pathlib import Path
from collections import defaultdict

# Mapeamento de strings atuais para chaves descritivas
STRING_MAPPING = {
    # Common elements
    'Pesquisar': 'common.search',
    'Limpar': 'common.clear',
    'Status': 'common.status',
    'Ativo': 'common.active',
    'Inativo': 'common.inactive',
    'Nome': 'common.name',
    'Código': 'common.code',
    'Editar': 'common.edit',
    'Excluir': 'common.delete',
    'Salvar': 'common.save',
    'Cancelar': 'common.cancel',
    'Voltar': 'common.back',
    'Confirmar': 'common.confirm',
    'Ações': 'common.actions',
    'Filtros': 'common.filters',
    'Todos': 'common.all',
    'Nenhum': 'common.none',
    'Encontrado': 'common.found',
    'Não encontrado': 'common.not_found',
    'Descrição': 'common.description',
    'Data': 'common.date',
    'Telefone': 'common.phone',
    'E-mail': 'common.email',
    'Senha': 'common.password',
    'Usuário': 'common.username',
    'Empresa': 'common.company',
    'País': 'common.country',
    'Endereço': 'common.address',
    'Cidade': 'common.city',
    'Estado': 'common.state',
    'CEP': 'common.zip_code',
    'Website': 'common.website',
    'Data de nascimento': 'common.birth_date',
    
    # Navigation
    'Dashboard': 'navigation.dashboard',
    'Clientes': 'navigation.customers',
    'Produtos': 'navigation.products',
    'Projetos': 'navigation.projects',
    'Utilitários': 'navigation.utilities',
    'Escalas': 'navigation.scales',
    'Tipos de Produto': 'navigation.product_types',
    'Categorias': 'navigation.categories',
    'Países': 'navigation.countries',
    'Perfil': 'navigation.profile',
    'Sair': 'navigation.logout',
    'Entrar': 'navigation.login',
    'Registrar': 'navigation.register',
    
    # Utilities
    'Escalas': 'utilities.scales.title',
    'Tipos de Produto': 'utilities.product_types.title',
    'Categorias': 'utilities.categories.title',
    'Países': 'utilities.countries.title',
    'Nova Escala': 'utilities.scales.add_new',
    'Novo Tipo de Produto': 'utilities.product_types.add_new',
    'Nova Categoria': 'utilities.categories.add_new',
    'Novo País': 'utilities.countries.add_new',
    'Editar Escala': 'utilities.scales.edit',
    'Editar Tipo de Produto': 'utilities.product_types.edit',
    'Editar Categoria': 'utilities.categories.edit',
    'Editar País': 'utilities.countries.edit',
    'Excluir Escala': 'utilities.scales.delete',
    'Excluir Tipo de Produto': 'utilities.product_types.delete',
    'Excluir Categoria': 'utilities.categories.delete',
    'Excluir País': 'utilities.countries.delete',
    'Alterar Status da Escala': 'utilities.scales.toggle_status',
    'Alterar Status do Tipo de Produto': 'utilities.product_types.toggle_status',
    'Alterar Status da Categoria': 'utilities.categories.toggle_status',
    'Alterar Status do País': 'utilities.countries.toggle_status',
    
    # Products
    'Produtos': 'products.title',
    'Novo Produto': 'products.add_new',
    'Editar Produto': 'products.edit',
    'Excluir Produto': 'products.delete',
    'Informações Básicas': 'products.basic_info',
    'Preços': 'products.prices',
    'Imagens': 'products.images',
    'Categoria': 'products.category',
    'Tipo': 'products.type',
    'Escala': 'products.scale',
    'Preço': 'products.price',
    'Preço Anual': 'products.yearly_price',
    'Moeda': 'products.currency',
    'Estoque': 'products.stock',
    'Peso': 'products.weight',
    'Dimensões': 'products.dimensions',
    'Altura': 'products.height',
    'Largura': 'products.width',
    'Profundidade': 'products.depth',
    
    # Customers
    'Clientes': 'customers.title',
    'Novo Cliente': 'customers.add_new',
    'Editar Cliente': 'customers.edit',
    'Excluir Cliente': 'customers.delete',
    'Nome Fantasia': 'customers.trade_name',
    'Razão Social': 'customers.company_name',
    'CNPJ': 'customers.cnpj',
    'CPF': 'customers.cpf',
    'RG': 'customers.rg',
    'Inscrição Estadual': 'customers.state_registration',
    'Inscrição Municipal': 'customers.municipal_registration',
    
    # Core
    'ForgeLock': 'core.brand_name',
    'Sistema de gestão empresarial': 'core.tagline',
    'Todos os direitos reservados.': 'core.copyright',
    'Bem-vindo ao ForgeLock': 'core.welcome_message',
    'Status da Assinatura': 'core.subscription.status',
    'Trial Ativo': 'core.subscription.trial_active',
    'Ativa': 'core.subscription.active',
    'EXPIRADA': 'core.subscription.expired',
    'dias restantes': 'core.subscription.days_remaining',
    'Trial': 'core.subscription.trial',
    'Plano Atual': 'core.subscription.current_plan',
    'Gerenciar Assinatura': 'core.subscription.manage',
    'Configurar Empresa': 'core.company.setup',
    'Meu Perfil': 'core.profile.title',
    'Informações Pessoais': 'core.profile.personal_info',
    'Não informado': 'core.profile.not_informed',
    
    # Forms and validation
    'Erro no formulário': 'forms.errors.title',
    'Campo obrigatório': 'forms.validation.required',
    'Formato inválido': 'forms.validation.invalid_format',
    'Já existe': 'forms.validation.already_exists',
    'Confirmação de senha': 'forms.validation.password_confirm',
    'As senhas não coincidem': 'forms.validation.password_mismatch',
    
    # Messages
    'Atenção!': 'messages.warning.title',
    'Sucesso!': 'messages.success.title',
    'Erro!': 'messages.error.title',
    'Informação': 'messages.info.title',
    'Tem certeza que deseja': 'messages.confirmation.prefix',
    'Esta ação não pode ser desfeita': 'messages.confirmation.irreversible',
    'Você tem certeza?': 'messages.confirmation.are_you_sure',
    
    # Time and dates
    'dias': 'time.days',
    'dias restantes': 'time.days_remaining',
    'dias para renovar': 'time.days_to_renew',
    'Durante a carência': 'time.grace_period.during',
    'Após o trial': 'time.trial.after',
    'Antes do bloqueio total': 'time.grace_period.before_block',
    
    # Actions
    'Criar Conta': 'actions.create_account',
    'Criar Conta Grátis': 'actions.create_free_account',
    'Começar Agora': 'actions.start_now',
    'Saiba Mais': 'actions.learn_more',
    'Escolher': 'actions.choose',
    'Alterar Senha': 'actions.change_password',
    'Nova Senha': 'actions.new_password',
    'Confirmar Nova Senha': 'actions.confirm_new_password',
    'Esqueceu sua senha?': 'actions.forgot_password',
    'Voltar ao Login': 'actions.back_to_login',
    'Voltar': 'actions.back',
    'Avançar': 'actions.next',
    'Avançar': 'actions.continue',
    
    # Features
    'Gestão de Clientes': 'features.customers.title',
    'Controle de Produtos': 'features.products.title',
    'Gestão de Projetos': 'features.projects.title',
    'Organize seus clientes': 'features.customers.description',
    'Gerencie estoque': 'features.products.description',
    'Acompanhe projetos': 'features.projects.description',
    'Por que escolher o ForgeLock?': 'features.why_choose.title',
    'Tudo que sua empresa precisa': 'features.why_choose.subtitle',
    'Planos e Preços': 'features.pricing.title',
    'Escolha o plano ideal': 'features.pricing.subtitle',
    'Mensal': 'features.pricing.monthly',
    'Anual': 'features.pricing.yearly',
    'usuário': 'features.pricing.user_singular',
    'usuários': 'features.pricing.user_plural',
    'Segurança STL': 'features.security.stl',
    'Pronto para começar?': 'features.cta.title',
    'Junte-se a centenas de empresas': 'features.cta.subtitle',
    
    # Specific utility strings
    'Nome ou descrição...': 'utilities.search.placeholder',
    'Nenhuma categoria encontrada': 'utilities.categories.not_found',
    'Nenhuma escala encontrada': 'utilities.scales.not_found',
    'Nenhum tipo de produto encontrado': 'utilities.product_types.not_found',
    'Nenhum país encontrado': 'utilities.countries.not_found',
    'Tente ajustar os filtros de pesquisa': 'utilities.search.adjust_filters',
    'ou adicione uma nova': 'utilities.search.or_add_new',
    'Sem descrição': 'utilities.items.no_description',
    'Confirmar Alteração de Status': 'utilities.status.confirm_change',
    'Tem certeza que deseja desativar': 'utilities.status.confirm_deactivate',
    'Tem certeza que deseja ativar': 'utilities.status.confirm_activate',
    'Desativar irá ocultar das listas': 'utilities.status.deactivate_warning',
    'mas não afetará dados já cadastrados': 'utilities.status.deactivate_note',
    'Ativar irá torná-lo disponível': 'utilities.status.activate_warning',
    'para uso em novos cadastros': 'utilities.status.activate_note',
    'Código não pode ser alterado': 'utilities.items.code_immutable',
    'Formatos aceitos: JPG, PNG, GIF': 'utilities.upload.accepted_formats',
    'Tamanho máximo: 2MB': 'utilities.upload.max_size',
}

def migrate_template_file(template_path):
    """Migra um arquivo de template para usar chaves descritivas"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Substituir todas as ocorrências de {% translate "string" %}
        for old_string, new_key in STRING_MAPPING.items():
            pattern = r'{%\s*translate\s+"' + re.escape(old_string) + r'"\s*%}'
            replacement = r'{% translate "' + new_key + r'" %}'
            
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made += 1
                print(f"   ✅ {old_string} → {new_key}")
        
        # Salvar arquivo se houver mudanças
        if changes_made > 0:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 {changes_made} mudanças salvas em {template_path.name}")
            return changes_made
        
        return 0
        
    except Exception as e:
        print(f"   ❌ Erro ao processar {template_path.name}: {e}")
        return 0

def migrate_python_file(python_path):
    """Migra um arquivo Python para usar chaves descritivas"""
    try:
        with open(python_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Substituir _("string") e gettext("string")
        for old_string, new_key in STRING_MAPPING.items():
            # Padrão para _("string")
            pattern1 = r'_\("' + re.escape(old_string) + r'"\)'
            replacement1 = r'_("' + new_key + r'")'
            
            # Padrão para gettext("string")
            pattern2 = r'gettext\("' + re.escape(old_string) + r'"\)'
            replacement2 = r'gettext("' + new_key + r'")'
            
            if re.search(pattern1, content):
                content = re.sub(pattern1, replacement1, content)
                changes_made += 1
                print(f"   ✅ {old_string} → {new_key} (_)")
            
            if re.search(pattern2, content):
                content = re.sub(pattern2, replacement2, content)
                changes_made += 1
                print(f"   ✅ {old_string} → {new_key} (gettext)")
        
        # Salvar arquivo se houver mudanças
        if changes_made > 0:
            with open(python_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 {changes_made} mudanças salvas em {python_path.name}")
            return changes_made
        
        return 0
        
    except Exception as e:
        print(f"   ❌ Erro ao processar {python_path.name}: {e}")
        return 0

def create_new_po_structure():
    """Cria nova estrutura de arquivos .po com chaves descritivas"""
    print("\n🔧 Criando nova estrutura de arquivos .po...")
    
    for lang in ['pt', 'en', 'es']:
        po_file = Path(f"locale/{lang}/LC_MESSAGES/django.po")
        if not po_file.exists():
            continue
            
        print(f"\n📝 Processando {lang}/LC_MESSAGES/django.po...")
        
        # Ler arquivo atual
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Criar backup
        backup_file = po_file.with_suffix('.po.backup')
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   💾 Backup criado: {backup_file.name}")
        
        # Substituir todas as chaves
        changes_made = 0
        for old_string, new_key in STRING_MAPPING.items():
            # Substituir msgid
            pattern = r'^msgid "' + re.escape(old_string) + r'"$'
            replacement = r'msgid "' + new_key + r'"'
            
            if re.search(pattern, content, re.MULTILINE):
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                changes_made += 1
                print(f"   ✅ {old_string} → {new_key}")
        
        # Salvar arquivo atualizado
        with open(po_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   💾 {changes_made} chaves migradas em {lang}")

def main():
    print("🚀 Migração para Chaves Descritivas - ForgeLock")
    print("=" * 60)
    
    total_changes = 0
    
    # 1. Migrar templates
    print("\n📁 Migrando templates HTML...")
    templates_dir = Path("templates")
    for template_file in templates_dir.rglob("*.html"):
        print(f"\n🔍 Processando: {template_file.name}")
        changes = migrate_template_file(template_file)
        total_changes += changes
    
    # 2. Migrar arquivos Python
    print("\n🐍 Migrando arquivos Python...")
    python_files = [
        "products/views.py",
        "products/forms.py",
        "customers/views.py",
        "customers/forms.py",
        "core/views.py",
        "core/forms.py",
    ]
    
    for py_file in python_files:
        if Path(py_file).exists():
            print(f"\n🔍 Processando: {py_file}")
            changes = migrate_python_file(Path(py_file))
            total_changes += changes
    
    # 3. Criar nova estrutura de .po
    create_new_po_structure()
    
    print(f"\n🎉 Migração concluída!")
    print(f"📊 Total de mudanças: {total_changes}")
    print(f"\n🔧 Próximos passos:")
    print(f"   1. Execute: python manage.py makemessages -l en -l es")
    print(f"   2. Execute: python scripts/auto_translate.py")
    print(f"   3. Execute: python manage.py compilemessages")
    print(f"   4. Teste a aplicação no navegador")
    
    return total_changes

if __name__ == "__main__":
    main()
