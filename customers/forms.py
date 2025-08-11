from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Customer
from core.models import Country


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'country', 'phone', 'email',
            'birth_date', 'document_number', 'social_network',
            'address', 'address_number', 'city', 'state', 'zip_code',
            'notes', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.name_reason_help')
            }),
            'country': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.phone_placeholder')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.email_placeholder')
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.document_placeholder')
            }),
            'social_network': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.social_placeholder')
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('customers.form.address_placeholder')
            }),
            'address_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.number_placeholder')
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.city_placeholder')
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.state_placeholder')
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('customers.form.zip_placeholder')
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('customers.form.notes_placeholder')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': _('customers.form.name_reason_required'),
            'country': _('customers.form.country_required'),
            'phone': _('customers.form.phone_required'),
            'email': _('customers.form.email_required'),
            'birth_date': _('customers.form.birth_date'),
            'document_number': _('customers.form.document_number'),
            'social_network': _('customers.form.social_network'),
            'address': _('customers.form.address'),
            'address_number': _('customers.form.address_number'),
            'city': _('customers.form.city'),
            'state': _('customers.form.state'),
            'zip_code': _('customers.form.zip_code'),
            'notes': _('customers.form.notes'),
            'is_active': _('customers.form.is_active')
        }
        help_texts = {
            'name': _('customers.form.name_reason_help'),
            'phone': _('customers.form.phone_help'),
            'email': _('customers.form.email_help'),
            'birth_date': _('customers.form.birth_date_help'),
            'document_number': _('customers.form.document_help'),
            'social_network': _('customers.form.social_network_help'),
            'address': _('customers.form.address_help'),
            'address_number': _('customers.form.address_number_help'),
            'notes': _('customers.form.notes_help')
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
                raise forms.ValidationError(_('customers.form.validation.phone_min_digits'))
        return phone
    
    def clean_document_number(self):
        """Validação básica do documento"""
        document = self.cleaned_data.get('document_number')
        if document:
            # Remove caracteres não numéricos
            doc_clean = ''.join(filter(str.isdigit, document))
            if len(doc_clean) not in [11, 14]:
                raise forms.ValidationError(_('customers.form.validation.document_length'))
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