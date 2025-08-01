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
    price = models.DecimalField(_("Preço"), max_digits=10, decimal_places=2)
    max_users = models.IntegerField(_("Máximo de usuários"), default=1)
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
        ordering = ['price']

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
        return None
    
    def calculate_trial_expiry(self, start_date=None):
        """Calcula a data de expiração do trial"""
        from django.utils import timezone
        if not self.is_trial:
            return None
        
        if not start_date:
            start_date = timezone.now()
        
        from datetime import timedelta
        return start_date + timedelta(days=self.trial_days)
    
    def get_price_for_currency(self, currency=None, billing_cycle='monthly'):
        """Retorna o preço para uma moeda específica e ciclo de cobrança"""
        if not currency:
            # Tentar usar moeda configurada no objeto
            currency = getattr(self, '_user_currency', 'USD')
        
        # Para trial, sempre retorna 0
        if self.is_trial:
            return 0
        
        try:
            # Para planos pagos, aplicar lógica de ciclo
            plan_price = self.prices.get(currency=currency, is_active=True)
            
            if billing_cycle == 'yearly':
                # Usar preço anual se definido, senão calcular automaticamente
                if plan_price.yearly_price:
                    return plan_price.yearly_price
                else:
                    # Calcular preço anual (12 meses com desconto)
                    from decimal import Decimal
                    yearly_price = plan_price.price * Decimal('12') * Decimal('0.83')  # 17% desconto (2 meses grátis)
                    return round(yearly_price, 2)
            else:
                return plan_price.price
        except:
            return self.price  # Fallback para preço padrão

    def get_yearly_price(self, currency=None):
        """Retorna o preço anual para uma moeda específica"""
        if not currency:
            # Tentar usar moeda configurada no objeto
            currency = getattr(self, '_user_currency', 'USD')
        return self.get_price_for_currency(currency, 'yearly')
    
    def get_currency_display(self, currency=None):
        """Retorna o símbolo da moeda"""
        if not currency:
            # Tentar usar moeda configurada no objeto
            currency = getattr(self, '_user_currency', 'USD')
        
        currency_symbols = {
            'BRL': 'R$',
            'USD': '$',
            'EUR': '€'
        }
        return currency_symbols.get(currency, currency)


class Company(models.Model):
    """Modelo para empresas"""
    name = models.CharField(_("Nome"), max_length=200)
    cnpj = models.CharField(_("CNPJ"), max_length=18, blank=True, null=True)
    email = models.EmailField(_("E-mail"))
    phone = models.CharField(_("Telefone"), max_length=20)
    address = models.TextField(_("Endereço"), blank=True)
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
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name=_("Empresa"), null=True, blank=True)
    date_of_birth = models.DateField(_("Data de nascimento"), default=timezone.now)
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


class Subscription(models.Model):
    """Modelo para assinaturas dos usuários"""
    STATUS_CHOICES = [
        ('trial', _('Trial')),
        ('active', _('Ativa')),
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

    def get_days_remaining(self):
        """Retorna dias restantes da assinatura"""
        if self.is_active():
            remaining = self.end_date - timezone.now()
            return max(0, remaining.days)
        return 0

    def get_price_for_cycle(self, currency=None):
        """Retorna o preço para o ciclo atual"""
        if not currency:
            from django.utils import translation
            current_language = translation.get_language()
            if current_language == 'pt':
                currency = 'BRL'
            elif current_language == 'es':
                currency = 'EUR'
            else:
                currency = 'USD'
        
        try:
            return self.plan.prices.get(currency=currency, is_active=True).price
        except PlanPrice.DoesNotExist:
            return self.plan.price

    def save(self, *args, **kwargs):
        """Override para calcular datas automaticamente"""
        if not self.start_date:
            self.start_date = timezone.now()
        
        if not self.end_date:
            if self.status == 'trial':
                self.end_date = self.start_date + timedelta(days=self.plan.trial_days)
            else:
                if self.billing_cycle == 'monthly':
                    self.end_date = self.start_date + timedelta(days=30)
                else:  # yearly
                    self.end_date = self.start_date + timedelta(days=365)
        
        if not self.next_billing_date and self.status != 'trial':
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
        return f"{self.plan.name} - {self.currency} {self.price}"


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
        return f"{self.username} - {self.ip_address} - {'Sucesso' if self.success else 'Falha'}"
