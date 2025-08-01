from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Country, Plan, Company, Account, LoginAttempt, Subscription, PlanPrice


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'ddi', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_users', 'max_customers', 'max_products', 'max_projects', 'has_stl_security', 'is_active']
    list_filter = ['is_active', 'has_stl_security']


@admin.register(PlanPrice)
class PlanPriceAdmin(admin.ModelAdmin):
    list_display = ['plan', 'currency', 'price', 'yearly_price', 'is_active']
    list_filter = ['currency', 'is_active', 'plan']
    search_fields = ['plan__name']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'country', 'is_active']
    list_filter = ['is_active', 'country']
    search_fields = ['name', 'email']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'is_active', 'created_at']
    list_filter = ['is_active', 'plan']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'billing_cycle', 'start_date', 'end_date', 'is_active']
    list_filter = ['status', 'billing_cycle', 'plan', 'auto_renew']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True
    is_active.short_description = _('Ativa')


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
        (_('Informações pessoais'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country', 'date_of_birth', 'website')}),
        (_('Empresa'), {'fields': ('company',)}),
        (_('Verificação'), {'fields': ('is_verified', 'verification_code', 'verification_expires_at')}),
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
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_verified', 'country']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']


admin.site.register(User, CustomUserAdmin)
