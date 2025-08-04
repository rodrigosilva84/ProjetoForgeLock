from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin customizado para clientes"""
    
    list_display = [
        'name', 'company', 'email', 'phone', 'country', 
        'is_active', 'created_at', 'get_age_display'
    ]
    
    list_filter = [
        'company', 'country', 'is_active', 'created_at',
        ('birth_date', admin.DateFieldListFilter),
    ]
    
    search_fields = [
        'name', 'email', 'phone', 'document_number', 
        'social_network', 'address', 'city', 'state'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Informações Básicas'), {
            'fields': ('company', 'name', 'country', 'is_active')
        }),
        (_('Contato'), {
            'fields': ('email', 'phone', 'social_network')
        }),
        (_('Documentação'), {
            'fields': ('birth_date', 'document_number'),
            'classes': ('collapse',)
        }),
        (_('Endereço'), {
            'fields': ('address', 'city', 'state', 'zip_code'),
            'classes': ('collapse',)
        }),
        (_('Observações'), {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25
    
    actions = ['activate_customers', 'deactivate_customers', 'export_customers']
    
    def get_age_display(self, obj):
        """Exibe a idade do cliente"""
        age = obj.get_age()
        if age is not None:
            return f"{age} anos"
        return "-"
    get_age_display.short_description = _('Idade')
    
    def get_queryset(self, request):
        """Filtra clientes por empresa se o usuário não for superuser"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Para usuários não-superuser, mostrar apenas clientes das suas empresas
        user_companies = request.user.companies.all()
        return qs.filter(company__in=user_companies)
    
    def activate_customers(self, request, queryset):
        """Ativar clientes selecionados"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            _('{} cliente(s) ativado(s) com sucesso.').format(updated)
        )
    activate_customers.short_description = _('Ativar clientes selecionados')
    
    def deactivate_customers(self, request, queryset):
        """Desativar clientes selecionados"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            _('{} cliente(s) desativado(s) com sucesso.').format(updated)
        )
    deactivate_customers.short_description = _('Desativar clientes selecionados')
    
    def export_customers(self, request, queryset):
        """Exportar clientes selecionados (placeholder)"""
        self.message_user(
            request, 
            _('Funcionalidade de exportação será implementada em breve.')
        )
    export_customers.short_description = _('Exportar clientes selecionados')
    
    def get_list_display(self, request):
        """Personaliza a exibição baseada no usuário"""
        list_display = list(super().get_list_display(request))
        
        # Se não for superuser, remover coluna company
        if not request.user.is_superuser:
            if 'company' in list_display:
                list_display.remove('company')
        
        return list_display
