from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from datetime import timedelta


class Country(models.Model):
    """Modelo para países"""
    name = models.CharField(_("Nome"), max_length=100)
    name_en = models.CharField(_("Nome (Inglês)"), max_length=100, blank=True)
    name_es = models.CharField(_("Nome (Espanhol)"), max_length=100, blank=True)
    code = models.CharField(_("Código"), max_length=3, unique=True)
    ddi = models.CharField(_("DDI"), max_length=5)
    flag = models.CharField(_("Bandeira"), max_length=10, blank=True)
    continent = models.CharField(_("Continente"), max_length=50, blank=True)
    region = models.CharField(_("Região"), max_length=50, blank=True)
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Países")
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_localized_name(self, language_code=None):
        """Retorna o nome do país no idioma especificado"""
        if not language_code:
            from django.utils import translation
            language_code = translation.get_language()
        
        if language_code == 'en' and self.name_en:
            return self.name_en
        elif language_code == 'es' and self.name_es:
            return self.name_es
        else:
            return self.name


class Plan(models.Model):
    """Modelo para planos de assinatura"""
    name = models.CharField(_("Nome"), max_length=100)
    name_en = models.CharField(_("Nome (Inglês)"), max_length=100, blank=True)
    name_es = models.CharField(_("Nome (Espanhol)"), max_length=100, blank=True)
    description = models.TextField(_("Descrição"))
    description_en = models.TextField(_("Descrição (Inglês)"), blank=True)
    description_es = models.TextField(_("Descrição (Espanhol)"), blank=True)
    max_users = models.IntegerField(_("Máximo de usuários"), default=1)
    max_companies = models.IntegerField(_("Máximo de empresas"), default=1)
    max_customers = models.IntegerField(_("Máximo de clientes"), default=100)
    max_products = models.IntegerField(_("Máximo de produtos"), default=50)
    max_projects = models.IntegerField(_("Máximo de projetos"), default=10)
    has_stl_security = models.BooleanField(_("Segurança STL"), default=False)
    is_trial = models.BooleanField(_("É plano trial"), default=False)
    trial_days = models.IntegerField(_("Dias de trial"), default=15)
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Plano")
        verbose_name_plural = _("Planos")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_localized_name(self, language_code=None):
        """Retorna o nome traduzido baseado no idioma"""
        if not language_code:
            from django.utils import translation
            language_code = translation.get_language()
        
        if language_code == 'en' and self.name_en:
            return self.name_en
        elif language_code == 'es' and self.name_es:
            return self.name_es
        else:
            return self.name

    def get_localized_description(self, language_code=None):
        """Retorna a descrição traduzida baseado no idioma"""
        if not language_code:
            from django.utils import translation
            language_code = translation.get_language()
        
        if language_code == 'en' and self.description_en:
            return self.description_en
        elif language_code == 'es' and self.description_es:
            return self.description_es
        else:
            return self.description
    
    def get_trial_duration_display(self):
        """Retorna a duração do trial formatada"""
        if self.is_trial:
            return f"{self.trial_days} dias"
        return "N/A"
    
    def calculate_trial_expiry(self, start_date=None):
        """Calcula a data de expiração do trial"""
        if not start_date:
            start_date = timezone.now()
        return start_date + timedelta(days=self.trial_days)
    
    def get_price_for_currency(self, currency=None, billing_cycle='monthly'):
        """Retorna o preço para a moeda especificada"""
        if not currency:
            currency = 'BRL'
        
        try:
            price_obj = self.prices.get(currency=currency, is_active=True)
            if billing_cycle == 'yearly' and price_obj.yearly_price:
                return price_obj.yearly_price
            return price_obj.price
        except PlanPrice.DoesNotExist:
            return 0  # Fallback se não encontrar preço
    
    def get_yearly_price(self, currency=None):
        """Retorna o preço anual para a moeda especificada"""
        if not currency:
            currency = 'BRL'
        
        try:
            price_obj = self.prices.get(currency=currency, is_active=True)
            return price_obj.yearly_price if price_obj.yearly_price else price_obj.price * 12
        except PlanPrice.DoesNotExist:
            return 0  # Fallback se não encontrar preço
    
    def get_currency_display(self, currency=None):
        """Retorna o símbolo da moeda"""
        if not currency:
            currency = 'BRL'
        
        currency_symbols = {
            'BRL': 'R$',
            'USD': '$',
            'EUR': '€',
        }
        return currency_symbols.get(currency, currency)


class Company(models.Model):
    """Modelo para empresas"""
    name = models.CharField(_("Nome"), max_length=200)
    cnpj = models.CharField(_("Documento"), max_length=18, blank=True, null=True)
    email = models.EmailField(_("E-mail"))
    phone = models.CharField(_("Telefone"), max_length=20)
    address = models.TextField(_("Endereço"), blank=True)
    address_number = models.CharField(_("Número"), max_length=20, blank=True)
    city = models.CharField(_("Cidade"), max_length=100, blank=True)
    state = models.CharField(_("Estado/Província"), max_length=100, blank=True)
    zip_code = models.CharField(_("CEP/Código Postal"), max_length=20, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_("País"))
    logo = models.ImageField(_("Logo"), upload_to='company_logos/', blank=True, null=True)
    description = models.TextField(_("Descrição"), blank=True)
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Empresa")
        verbose_name_plural = _("Empresas")
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Modelo de usuário customizado"""
    email = models.EmailField(_("E-mail"), unique=True)
    phone_number = models.CharField(_("Telefone"), max_length=20, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_("País"))
    # Removido: company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name=_("Empresa"), null=True, blank=True)
    companies = models.ManyToManyField(Company, through='UserCompany', verbose_name=_("Empresas"))
    birth_date = models.DateField(_("Data de nascimento"), default=timezone.now)
    address = models.TextField(_("Endereço"), blank=True)
    address_number = models.CharField(_("Número"), max_length=20, blank=True)
    city = models.CharField(_("Cidade"), max_length=100, blank=True)
    state = models.CharField(_("Estado/Província"), max_length=100, blank=True)
    zip_code = models.CharField(_("CEP/Código Postal"), max_length=20, blank=True)
    website = models.URLField(_("Site pessoal"), blank=True)
    is_verified = models.BooleanField(_("Verificado"), default=False)
    is_first_access = models.BooleanField(_("Primeiro acesso"), default=True)
    verification_code = models.CharField(_("Código de verificação"), max_length=10, blank=True)
    verification_expires_at = models.DateTimeField(_("Expiração da verificação"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.email
    
    def get_primary_company(self):
        """Retorna a empresa principal do usuário (primeira criada)"""
        return self.companies.first()
    
    def get_companies_with_roles(self):
        """Retorna as empresas do usuário com seus roles"""
        return self.usercompany_set.select_related('company').all()
    
    def can_access_company(self, company):
        """Verifica se o usuário pode acessar uma empresa específica"""
        return self.usercompany_set.filter(company=company, is_active=True).exists()
    
    def get_role_in_company(self, company):
        """Retorna o role do usuário em uma empresa específica"""
        try:
            user_company = self.usercompany_set.get(company=company, is_active=True)
            return user_company.role
        except UserCompany.DoesNotExist:
            return None


class UserCompany(models.Model):
    """Modelo intermediário para relacionamento User-Company com roles e permissions"""
    ROLE_CHOICES = [
        ('owner', _('Proprietário')),
        ('admin', _('Administrador')),
        ('manager', _('Gerente')),
        ('member', _('Membro')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Usuário"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("Empresa"))
    role = models.CharField(_("Função"), max_length=20, choices=ROLE_CHOICES, default='member')
    permissions = models.JSONField(_("Permissões"), default=dict, blank=True)
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Usuário-Empresa")
        verbose_name_plural = _("Usuários-Empresas")
        unique_together = ['user', 'company']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.company.name} ({self.get_role_display()})"
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        if self.role == 'owner':
            return True
        return self.permissions.get(permission, False)
    
    def get_permissions(self):
        """Retorna as permissões baseadas no role"""
        base_permissions = {
            'owner': ['all'],
            'admin': ['manage_users', 'manage_company', 'view_reports', 'manage_data'],
            'manager': ['view_reports', 'manage_data', 'view_users'],
            'member': ['view_data', 'create_data'],
        }
        return base_permissions.get(self.role, [])


class Account(models.Model):
    """Modelo para conta do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name=_("Plano"))
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Conta")
        verbose_name_plural = _("Contas")

    def __str__(self):
        return f"Conta de {self.user.email}"

    def get_active_subscription(self):
        """Retorna a assinatura ativa do usuário"""
        return self.user.subscriptions.filter(status__in=['trial', 'active']).first()

    def is_trial_active(self):
        """Verifica se o trial ainda está ativo"""
        subscription = self.get_active_subscription()
        if subscription and subscription.status == 'trial':
            return timezone.now() < subscription.end_date
        return False

    def get_trial_days_remaining(self):
        """Retorna dias restantes do trial"""
        subscription = self.get_active_subscription()
        if subscription and subscription.status == 'trial':
            remaining = subscription.end_date - timezone.now()
            return max(0, remaining.days)
        return 0
    
    def can_add_company(self):
        """Verifica se o usuário pode adicionar mais empresas baseado no plano"""
        current_companies = self.user.companies.count()
        return current_companies < self.plan.max_companies
    
    def can_add_user_to_company(self, company):
        """Verifica se o usuário pode adicionar mais usuários a uma empresa"""
        current_users = company.user_set.count()
        return current_users < self.plan.max_users


class Subscription(models.Model):
    """Modelo para assinaturas dos usuários"""
    STATUS_CHOICES = [
        ('trial', _('Trial')),
        ('active', _('Ativa')),
        ('grace_period', _('Período de Carência')),
        ('cancelled', _('Cancelada')),
        ('expired', _('Expirada')),
    ]
    
    BILLING_CYCLE_CHOICES = [
        ('monthly', _('Mensal')),
        ('yearly', _('Anual')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name=_("Usuário"))
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name=_("Plano"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='trial')
    billing_cycle = models.CharField(_("Ciclo de cobrança"), max_length=20, choices=BILLING_CYCLE_CHOICES, default='monthly')
    start_date = models.DateTimeField(_("Data de início"))
    end_date = models.DateTimeField(_("Data de fim"))
    next_billing_date = models.DateTimeField(_("Próxima cobrança"), null=True, blank=True)
    grace_period_until = models.DateTimeField(_("Fim do período de carência"), null=True, blank=True)
    last_notification_sent = models.DateTimeField(_("Última notificação enviada"), null=True, blank=True)
    auto_renew = models.BooleanField(_("Renovação automática"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Assinatura")
        verbose_name_plural = _("Assinaturas")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.get_status_display()})"

    def is_active(self):
        """Verifica se a assinatura está ativa"""
        return self.status in ['trial', 'active'] and timezone.now() < self.end_date

    def is_in_grace_period(self):
        """Verifica se está no período de carência"""
        if self.status == 'grace_period' and self.grace_period_until:
            return timezone.now() <= self.grace_period_until
        return False

    def can_access_full_features(self):
        """Verifica se pode acessar todas as funcionalidades"""
        return self.is_active() and not self.is_in_grace_period()

    def can_access_read_only(self):
        """Verifica se pode acessar apenas visualização"""
        return self.is_active() or self.is_in_grace_period()

    def get_days_remaining(self):
        """Retorna dias restantes da assinatura"""
        if self.is_active():
            remaining = self.end_date - timezone.now()
            return max(0, remaining.days)
        return 0

    def get_grace_period_days_remaining(self):
        """Retorna dias restantes do período de carência"""
        if self.is_in_grace_period():
            remaining = self.grace_period_until - timezone.now()
            return max(0, remaining.days)
        return 0

    def get_price_for_cycle(self, currency=None):
        """Retorna o preço para o ciclo de cobrança atual"""
        if not currency:
            currency = 'BRL'
        
        try:
            price_obj = self.plan.prices.get(currency=currency, is_active=True)
            if self.billing_cycle == 'yearly' and price_obj.yearly_price:
                return price_obj.yearly_price
            return price_obj.price
        except PlanPrice.DoesNotExist:
            if self.billing_cycle == 'yearly':
                return self.plan.price * 12
            return self.plan.price

    def save(self, *args, **kwargs):
        """Override do save para calcular datas automaticamente"""
        if not self.start_date:
            self.start_date = timezone.now()
        
        if not self.end_date:
            if self.status == 'trial':
                self.end_date = self.plan.calculate_trial_expiry(self.start_date)
            else:
                # Para assinaturas pagas, calcular baseado no billing_cycle
                if self.billing_cycle == 'yearly':
                    self.end_date = self.start_date + timedelta(days=365)
                else:
                    self.end_date = self.start_date + timedelta(days=30)
        
        if not self.next_billing_date:
            self.next_billing_date = self.end_date
        
        super().save(*args, **kwargs)


class PlanPrice(models.Model):
    """Modelo para preços dos planos por moeda"""
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='prices', verbose_name=_("Plano"))
    currency = models.CharField(_("Moeda"), max_length=3, choices=[
        ('BRL', 'Real Brasileiro'),
        ('USD', 'Dólar Americano'),
        ('EUR', 'Euro'),
    ])
    price = models.DecimalField(_("Preço Mensal"), max_digits=10, decimal_places=2)
    yearly_price = models.DecimalField(_("Preço Anual"), max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['plan', 'currency']
        verbose_name = _("Preço do Plano")
        verbose_name_plural = _("Preços dos Planos")

    def __str__(self):
        return f"{self.plan.name} - {self.currency} ({self.price})"


class LoginAttempt(models.Model):
    """Modelo para rastrear tentativas de login"""
    username = models.CharField(_("Nome de usuário"), max_length=150)
    ip_address = models.GenericIPAddressField(_("Endereço IP"))
    success = models.BooleanField(_("Sucesso"), default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(_("User Agent"), blank=True)

    class Meta:
        verbose_name = _("Tentativa de Login")
        verbose_name_plural = _("Tentativas de Login")
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.username} - {'Sucesso' if self.success else 'Falha'} - {self.timestamp}"
