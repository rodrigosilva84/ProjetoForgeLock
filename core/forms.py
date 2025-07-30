from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Country, Company

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Form para registro de usuário"""
    email = forms.EmailField(
        label=_("E-mail *"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Seu email")}),
        error_messages={
            'unique': _('Já existe um usuário com este e-mail.')
        }
    )
    first_name = forms.CharField(
        label=_("Nome *"),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Seu nome")})
    )
    last_name = forms.CharField(
        label=_("Sobrenome *"),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Seu sobrenome")})
    )
    phone_number = forms.CharField(
        label=_("Telefone (DDD + Número) *"),
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("(11) 99999-9999")}),
        error_messages={
            'unique': _('Já existe um usuário com este telefone.')
        }
    )
    country = forms.ModelChoiceField(
        label=_("País *"),
        queryset=Country.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=_("Selecione um país")
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _("Nome de usuário")})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _("Senha")})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _("Confirme a senha")})
        
        # Traduzir labels
        self.fields['username'].label = _("Nome de usuário *")
        self.fields['password1'].label = _("Senha *")
        self.fields['password2'].label = _("Confirme a senha *")
        
        # Help texts
        self.fields['username'].help_text = _("O nome de usuário pode ter no máximo 150 caracteres. Podem ser utilizados letras, dígitos e símbolos especiais. Exemplo: joao.silva, user123, admin@test")
        self.fields['password1'].help_text = _("Sua senha deve conter pelo menos 8 caracteres.")
        self.fields['password2'].help_text = _("Digite a mesma senha novamente para verificação.")
        
        # Personalizar as opções do campo country para usar nomes localizados
        from django.utils import translation
        current_language = translation.get_language()
        
        # Criar choices personalizados com nomes localizados
        country_choices = [('', _("Selecione um país"))]
        for country in Country.objects.filter(is_active=True):
            country_choices.append((country.id, country.get_localized_name(current_language)))
        
        self.fields['country'].choices = country_choices


class UserLoginForm(forms.Form):
    """Form para login de usuário"""
    username = forms.CharField(
        label=_("Nome de usuário ou E-mail"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Nome de usuário ou e-mail")})
    )
    password = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Sua senha")})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Nome de usuário ou E-mail")


class SMSVerificationForm(forms.Form):
    """Form para verificação SMS"""
    verification_code = forms.CharField(
        label=_("Código de verificação"),
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000000',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['verification_code'].label = _("Código de verificação")


class CompanyForm(forms.ModelForm):
    """Form para configuração de empresa"""
    class Meta:
        model = Company
        fields = ['name', 'cnpj', 'email', 'phone', 'address', 'country', 'logo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contato@empresa.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Endereço completo'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição da empresa'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traduzir labels
        self.fields['name'].label = _("Nome da empresa")
        self.fields['cnpj'].label = _("CNPJ")
        self.fields['email'].label = _("E-mail")
        self.fields['phone'].label = _("Telefone")
        self.fields['address'].label = _("Endereço")
        self.fields['country'].label = _("País")
        self.fields['logo'].label = _("Logo")
        self.fields['description'].label = _("Descrição")
        
        # Filtrar países ativos
        self.fields['country'].queryset = Country.objects.filter(is_active=True)
        self.fields['country'].empty_label = _("Selecione um país")