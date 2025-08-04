from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Customer
from core.models import Country


class CustomerForm(forms.ModelForm):
    """Formulário para criação e edição de clientes"""
    
    class Meta:
        model = Customer
        fields = [
            'name', 'country', 'phone', 'email',
            'birth_date', 'document_number', 'social_network',
            'address', 'city', 'state', 'zip_code',
            'notes', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome completo ou razão social')
            }),
            'country': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('(11) 99999-9999')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('cliente@exemplo.com')
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('000.000.000-00 ou 00.000.000/0000-00')
            }),
            'social_network': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('@usuario ou link da rede social')
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Endereço completo')
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Cidade')
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Estado/Província')
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('00000-000')
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Observações sobre o cliente')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': _('Nome/Razão Social *'),
            'country': _('País *'),
            'phone': _('Telefone *'),
            'email': _('E-mail *'),
            'birth_date': _('Data de Nascimento'),
            'document_number': _('CPF/CNPJ'),
            'social_network': _('Instagram/Rede Social'),
            'address': _('Endereço'),
            'city': _('Cidade'),
            'state': _('Estado/Província'),
            'zip_code': _('CEP/Código Postal'),
            'notes': _('Observações'),
            'is_active': _('Cliente ativo')
        }
        help_texts = {
            'name': _('Nome completo para pessoa física ou razão social para pessoa jurídica'),
            'phone': _('Inclua o código do país se necessário'),
            'email': _('E-mail válido para comunicações'),
            'birth_date': _('Opcional - útil para campanhas personalizadas'),
            'document_number': _('CPF para pessoa física ou CNPJ para pessoa jurídica'),
            'social_network': _('Instagram, Facebook, LinkedIn ou outra rede social'),
            'address': _('Endereço completo para envio de materiais'),
            'notes': _('Informações adicionais sobre o cliente')
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Definir campos obrigatórios
        required_fields = ['name', 'country', 'phone', 'email']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
        
        # Definir campos opcionais
        optional_fields = ['birth_date', 'document_number', 'social_network', 
                         'address', 'city', 'state', 'zip_code', 'notes']
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False
        
        # Ordenar países por nome
        if 'country' in self.fields:
            self.fields['country'].queryset = Country.objects.filter(is_active=True).order_by('name')
    
    def clean_phone(self):
        """Validação básica do telefone"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove caracteres não numéricos para validação
            phone_clean = ''.join(filter(str.isdigit, phone))
            if len(phone_clean) < 10:
                raise forms.ValidationError(_('Telefone deve ter pelo menos 10 dígitos'))
        return phone
    
    def clean_document_number(self):
        """Validação básica do documento"""
        document = self.cleaned_data.get('document_number')
        if document:
            # Remove caracteres não numéricos
            doc_clean = ''.join(filter(str.isdigit, document))
            if len(doc_clean) not in [11, 14]:
                raise forms.ValidationError(_('CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos'))
        return document
    
    def clean_email(self):
        """Validação do e-mail"""
        email = self.cleaned_data.get('email')
        if email:
            # Verificar se já existe um cliente com este e-mail na mesma empresa
            if hasattr(self, 'instance') and self.instance.pk:
                # Editando cliente existente
                existing = Customer.objects.filter(
                    company=self.instance.company,
                    email=email
                ).exclude(pk=self.instance.pk)
            else:
                # Criando novo cliente - não podemos verificar empresa ainda
                # A validação será feita na view
                pass
        
        return email 