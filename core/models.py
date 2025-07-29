from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


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
    description = models.TextField(_("Descrição"))
    price = models.DecimalField(_("Preço"), max_digits=10, decimal_places=2)
    max_users = models.IntegerField(_("Máximo de usuários"), default=1)
    max_customers = models.IntegerField(_("Máximo de clientes"), default=100)
    max_products = models.IntegerField(_("Máximo de produtos"), default=50)
    max_projects = models.IntegerField(_("Máximo de projetos"), default=10)
    has_stl_security = models.BooleanField(_("Segurança STL"), default=False)
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Plano")
        verbose_name_plural = _("Planos")
        ordering = ['price']

    def __str__(self):
        return self.name


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
    phone_number = models.CharField(_("Telefone"), max_length=20)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_("País"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("Empresa"), null=True, blank=True)
    is_verified = models.BooleanField(_("Verificado"), default=False)
    verification_code = models.CharField(_("Código de verificação"), max_length=10, blank=True)
    verification_expires_at = models.DateTimeField(_("Expiração da verificação"), null=True, blank=True)
    trial_expires = models.DateTimeField(_("Expiração do trial"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.email

    def is_trial_active(self):
        """Verifica se o trial ainda está ativo"""
        if not self.trial_expires:
            return False
        return timezone.now() < self.trial_expires


class Account(models.Model):
    """Modelo para conta do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name=_("Plano"))
    is_active = models.BooleanField(_("Ativo"), default=True)
    trial_expires_at = models.DateTimeField(_("Expiração do trial"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Conta")
        verbose_name_plural = _("Contas")

    def __str__(self):
        return f"Conta de {self.user.username}"


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
