from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Country, Plan, Company, Account


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'company')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'country', 'company')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações pessoais'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country')}),
        (_('Empresa'), {'fields': ('company',)}),
        (_('Verificação'), {'fields': ('is_verified', 'verification_code', 'verification_expires', 'trial_expires')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'country'),
        }),
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'ddi', 'flag', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_users', 'max_customers', 'max_products', 'max_projects', 'has_stl_security', 'is_active')
    list_filter = ('is_active', 'has_stl_security')
    search_fields = ('name',)
    ordering = ('price',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'email', 'phone', 'country', 'is_active')
    list_filter = ('is_active', 'country')
    search_fields = ('name', 'cnpj', 'email')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'created_at')
    list_filter = ('is_active', 'plan')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
