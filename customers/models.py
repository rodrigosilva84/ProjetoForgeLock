from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Company, Country

class Customer(models.Model):
    """Modelo para clientes das empresas"""
    
    # Campos obrigatórios
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("Empresa"))
    name = models.CharField(_("Nome/Razão Social"), max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_("País"))
    phone = models.CharField(_("Telefone"), max_length=20)
    email = models.EmailField(_("E-mail"))
    
    # Campos opcionais
    birth_date = models.DateField(_("Data de Nascimento"), null=True, blank=True)
    document_number = models.CharField(_("CPF/CNPJ"), max_length=20, blank=True)
    social_network = models.CharField(_("Instagram/Rede Social"), max_length=100, blank=True)
    
    # Endereço (opcional)
    address = models.TextField(_("Endereço"), blank=True)
    city = models.CharField(_("Cidade"), max_length=100, blank=True)
    state = models.CharField(_("Estado/Província"), max_length=100, blank=True)
    zip_code = models.CharField(_("CEP/Código Postal"), max_length=20, blank=True)
    
    # Controle
    notes = models.TextField(_("Observações"), blank=True)
    is_active = models.BooleanField(_("Ativo"), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")
        ordering = ['name']
        unique_together = ['company', 'name']  # Nome único por empresa
    
    def __str__(self):
        return self.name
    
    def get_age(self):
        """Retorna a idade do cliente baseada na data de nascimento"""
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def get_document_display(self):
        """Retorna o documento formatado se existir"""
        if self.document_number:
            # Formatação básica para CPF/CNPJ
            doc = self.document_number.replace('.', '').replace('-', '').replace('/', '')
            if len(doc) == 11:  # CPF
                return f"{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:]}"
            elif len(doc) == 14:  # CNPJ
                return f"{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:]}"
            else:
                return self.document_number
        return ""
