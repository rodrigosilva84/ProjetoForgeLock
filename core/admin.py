from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .models import User, Country, Plan, Company, Account, LoginAttempt, Subscription, PlanPrice, UserCompany


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'ddi', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_users', 'max_companies', 'max_customers', 'max_products', 'max_projects', 'has_stl_security', 'is_active']
    list_filter = ['is_active', 'has_stl_security']


@admin.register(PlanPrice)
class PlanPriceAdmin(admin.ModelAdmin):
    list_display = ['plan', 'currency', 'price', 'yearly_price', 'is_active']
    list_filter = ['currency', 'is_active', 'plan']
    search_fields = ['plan__name']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'country', 'is_active', 'users_count']
    list_filter = ['is_active', 'country']
    search_fields = ['name', 'email']
    readonly_fields = ['users_list']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'cnpj', 'email', 'phone', 'address', 'country', 'logo', 'description', 'is_active')
        }),
        (_('Usuários Associados'), {
            'fields': ('users_list',),
            'classes': ('collapse',),
            'description': _('Lista de usuários que têm acesso a esta empresa')
        }),
    )
    
    def users_count(self, obj):
        return obj.user_set.count()
    users_count.short_description = _('Usuários')
    
    def users_list(self, obj):
        """Exibe a lista de usuários associados à empresa com seus roles"""
        from .models import UserCompany
        
        user_companies = UserCompany.objects.filter(company=obj, is_active=True).select_related('user')
        
        if not user_companies:
            return _('Nenhum usuário associado')
        
        html = '<ul>'
        for uc in user_companies:
            role_display = uc.get_role_display()
            html += f'<li><strong>{uc.user.username}</strong> ({uc.user.email}) - <em>{role_display}</em></li>'
        html += '</ul>'
        
        return mark_safe(html)
    users_list.short_description = _('Usuários da Empresa')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'is_active', 'created_at']
    list_filter = ['is_active', 'plan']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'billing_cycle', 'start_date', 'end_date', 'is_active', 'grace_period_until']
    list_filter = ['status', 'billing_cycle', 'plan', 'auto_renew']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['check_subscription_status', 'force_grace_period', 'send_notification', 'check_all_subscriptions']
    
    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True
    is_active.short_description = _('Ativa')
    
    def check_subscription_status(self, request, queryset):
        """Verifica o status da assinatura selecionada"""
        from django.utils import timezone
        from datetime import timedelta
        
        updated = 0
        for subscription in queryset:
            # Verificar se expirou
            if subscription.status in ['active', 'trial'] and subscription.end_date <= timezone.now():
                subscription.status = 'grace_period'
                subscription.grace_period_until = timezone.now() + timedelta(days=15)
                subscription.save()
                updated += 1
                self.message_user(request, f'Assinatura de {subscription.user.email} movida para período de carência.')
            
            # Verificar se carência acabou
            elif subscription.status == 'grace_period' and subscription.grace_period_until and subscription.grace_period_until <= timezone.now():
                subscription.status = 'expired'
                subscription.save()
                updated += 1
                self.message_user(request, f'Assinatura de {subscription.user.email} expirada (carência encerrada).')
        
        if updated == 0:
            self.message_user(request, 'Nenhuma assinatura precisava de atualização.')
        else:
            self.message_user(request, f'{updated} assinatura(s) atualizada(s).')
    
    check_subscription_status.short_description = "Verificar status da assinatura"
    
    def force_grace_period(self, request, queryset):
        """Força período de carência para assinaturas selecionadas"""
        from django.utils import timezone
        from datetime import timedelta
        
        updated = 0
        for subscription in queryset:
            if subscription.status in ['active', 'trial']:
                subscription.status = 'grace_period'
                subscription.grace_period_until = timezone.now() + timedelta(days=15)
                subscription.save()
                updated += 1
        
        self.message_user(request, f'{updated} assinatura(s) movida(s) para período de carência.')
    
    force_grace_period.short_description = "Forçar período de carência"
    
    def send_notification(self, request, queryset):
        """Envia notificação para assinaturas selecionadas"""
        from django.utils import timezone
        
        sent = 0
        for subscription in queryset:
            if subscription.status in ['active', 'trial']:
                subscription.last_notification_sent = timezone.now()
                subscription.save()
                sent += 1
                # TODO: Implementar envio real de email/SMS
                self.message_user(request, f'Notificação enviada para {subscription.user.email}.')
        
        if sent == 0:
            self.message_user(request, 'Nenhuma notificação foi enviada.')
        else:
            self.message_user(request, f'{sent} notificação(ões) enviada(s).')
    
    send_notification.short_description = "Enviar notificação"
    
    def check_all_subscriptions(self, request, queryset):
        """Verifica todas as assinaturas do sistema"""
        from django.core.management import call_command
        from io import StringIO
        
        # Capturar output do comando
        out = StringIO()
        call_command('check_subscriptions', '--dry-run', stdout=out)
        
        # Mostrar resultado
        result = out.getvalue()
        self.message_user(request, f'Verificação concluída. Resultado: {result}')
    
    check_all_subscriptions.short_description = "Verificar todas as assinaturas"


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip_address', 'success', 'timestamp']
    list_filter = ['success', 'timestamp', 'ip_address']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False  # Não permitir adicionar manualmente


# Configuração personalizada do UserAdmin
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações pessoais'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country', 'birth_date', 'website')}),
        (_('Verificação'), {'fields': ('is_verified', 'verification_code', 'verification_expires_at')}),
        (_('Empresas'), {
            'fields': ('companies_list',),
            'classes': ('collapse',),
            'description': _('Empresas às quais este usuário tem acesso')
        }),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'companies_count']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_verified', 'country']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    readonly_fields = ['companies_list']
    
    def companies_count(self, obj):
        return obj.companies.count()
    companies_count.short_description = _('Empresas')
    
    def companies_list(self, obj):
        """Exibe a lista de empresas do usuário com seus roles"""
        from .models import UserCompany
        
        user_companies = UserCompany.objects.filter(user=obj, is_active=True).select_related('company')
        
        if not user_companies:
            return _('Nenhuma empresa associada')
        
        html = '<ul>'
        for uc in user_companies:
            role_display = uc.get_role_display()
            html += f'<li><strong>{uc.company.name}</strong> - <em>{role_display}</em></li>'
        html += '</ul>'
        
        return mark_safe(html)
    companies_list.short_description = _('Empresas do Usuário')


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'company__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


admin.site.register(User, CustomUserAdmin)
