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
        required=True,
        error_messages={
            'unique': _('Já existe um usuário com este telefone.')
        }
    )
    country = forms.ModelChoiceField(
        label=_("País *"),
        queryset=Country.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=_("Selecione um país"),
        required=True
    )
    date_of_birth = forms.DateField(
        label=_("Data de nascimento *"),
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'birth_date', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _("Nome de usuário")})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _("common.password")})
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
        
        # Forçar atualização das choices quando o idioma muda
        self.fields['country'].widget.attrs['data-language'] = current_language
        
        # Adicionar parâmetro de cache-busting para forçar atualização
        self.fields['country'].widget.attrs['data-cache-bust'] = current_language


class UserLoginForm(forms.Form):
    """Form para login de usuário"""
    username = forms.CharField(
        label=_("Nome de usuário ou E-mail"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Nome de usuário ou e-mail")})
    )
    password = forms.CharField(
        label=_("common.password"),
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


class UserProfileForm(forms.ModelForm):
    """Form para completar perfil do usuário"""
    website = forms.URLField(
        label=_("Site pessoal"),
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': _("https://meusite.com")}),
        help_text=_("Opcional. Seu site pessoal ou portfólio.")
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'address', 'address_number', 'city', 'state', 'zip_code', 'website']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Endereço completo')}),
            'address_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Número')}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Cidade')}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Estado/Província')}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('00000-000')}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': _('https://meusite.com')})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removendo traduções duplicadas - agora usamos template translations
        
        # Configurar labels e help texts
        self.fields['birth_date'].label = _("common.birth_date")
        self.fields['birth_date'].help_text = _("Sua data de nascimento.")


class CompanyForm(forms.ModelForm):
    """Form para configuração de empresa"""
    use_registration_data = forms.BooleanField(
        label=_("Usar dados do meu registro"),
        required=False,
        initial=False,
        help_text=_("Marque para usar automaticamente seus dados de registro nos campos da empresa.")
    )
    
    class Meta:
        model = Company
        fields = ['name', 'cnpj', 'email', 'phone', 'address', 'address_number', 'city', 'state', 'zip_code', 'country', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nome da empresa ou nome fantasia')}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('CNPJ, CPF, RG, Passaporte, etc. (opcional)')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contato@empresa.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Endereço completo (opcional)')}),
            'address_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Número')}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Cidade')}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Estado/Província')}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('00000-000')}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Armazenar o usuário para uso na validação
        self.user = user
        
        # Traduzir labels
        self.fields['name'].label = _("Nome da empresa")
        self.fields['cnpj'].label = _("Documento")
        self.fields['email'].label = _("common.email")
        self.fields['phone'].label = _("common.phone")
        self.fields['address'].label = _("common.address")
        self.fields['country'].label = _("common.country")
        self.fields['logo'].label = _("Logo")
        
        # Filtrar países ativos
        self.fields['country'].queryset = Country.objects.filter(is_active=True)
        self.fields['country'].empty_label = _("Selecione um país")
        
        # Se temos um usuário e o flag está marcado, preencher automaticamente
        if user and self.data.get('use_registration_data') == 'on':
            self._prefill_with_user_data(user)
    
    def _prefill_with_user_data(self, user):
        """Preenche os campos com dados do usuário"""
        # Nome da empresa = Nome + Sobrenome
        if user.first_name and user.last_name:
            self.fields['name'].initial = f"{user.first_name} {user.last_name}"
        elif user.first_name:
            self.fields['name'].initial = user.first_name
        elif user.last_name:
            self.fields['name'].initial = user.last_name
        
        # Documento fica em branco (opcional)
        self.fields['cnpj'].initial = ""
        
        # País = País do usuário
        if user.country:
            self.fields['country'].initial = user.country
        
        # E-mail = E-mail do usuário
        if user.email:
            self.fields['email'].initial = user.email
        
        # Telefone = Telefone do usuário
        if user.phone_number:
            self.fields['phone'].initial = user.phone_number
        
        # Endereço fica em branco (opcional)
        self.fields['address'].initial = ""
        
        # Logo fica em branco (opcional)
        self.fields['logo'].initial = ""
    
    def clean(self):
        """Validação personalizada para garantir que campos obrigatórios sejam preenchidos"""
        cleaned_data = super().clean()
        
        # Se o checkbox está marcado, usar dados do usuário
        use_registration_data = self.data.get('use_registration_data') == 'on' if self.data else False
        
        if use_registration_data:
            user = self.user if hasattr(self, 'user') else None
            if user:
                if not cleaned_data.get('name'):
                    cleaned_data['name'] = f"{user.first_name} {user.last_name}".strip()
                if not cleaned_data.get('email'):
                    cleaned_data['email'] = user.email
                if not cleaned_data.get('phone'):
                    cleaned_data['phone'] = user.phone_number
                if not cleaned_data.get('country'):
                    cleaned_data['country'] = user.country
        
        return cleaned_data