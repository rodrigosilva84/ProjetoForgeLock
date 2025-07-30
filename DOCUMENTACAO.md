# 📚 Documentação ForgeLock Web Platform

## 🎯 Visão Geral

O **ForgeLock** é uma plataforma web para gestão de projetos de impressão 3D, com foco em segurança de arquivos STL e controle de acesso. O sistema oferece planos de assinatura com preços baseados em geolocalização.

---

## 🌍 Internacionalização (i18n)

### Idiomas Suportados
- **Português (pt)** - Idioma padrão
- **Inglês (en)** 
- **Espanhol (es)**

### Funcionalidades
- ✅ Seletor de idioma no header
- ✅ Tradução completa de interfaces
- ✅ Mensagens de erro traduzidas
- ✅ Formulários traduzidos
- ✅ Sistema de mensagens (success, error, warning)

### Arquivos de Tradução
```
locale/
├── pt/LC_MESSAGES/django.po
├── en/LC_MESSAGES/django.po
└── es/LC_MESSAGES/django.po
```

### Comandos de Tradução
```bash
# Compilar traduções
python manage.py compilemessages

# Extrair strings para tradução
python manage.py makemessages -l pt
python manage.py makemessages -l en
python manage.py makemessages -l es
```

---

## 🔐 Sistema de Autenticação e Segurança

### Registro de Usuário
- ✅ Validação de e-mail único
- ✅ Validação de telefone único
- ✅ Verificação SMS via Twilio Verify
- ✅ Código de verificação com expiração
- ✅ Redirecionamento para configuração de empresa

### Login e Segurança
- ✅ Sistema de tentativas de login
- ✅ Bloqueio temporário (1 minuto)
- ✅ Limpeza automática de tentativas
- ✅ Mensagens específicas de erro
- ✅ Tracking no Django Admin

### Modelo de Segurança
```python
class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Configurações de Segurança
- **Tentativas máximas**: 5
- **Tempo de bloqueio**: 1 minuto
- **Limpeza automática**: 15 minutos

---

## 📱 Verificação SMS

### Integração Twilio
- ✅ Twilio Verify API
- ✅ Código de 6 dígitos
- ✅ Expiração automática
- ✅ Reenvio de código
- ✅ Validação em tempo real

### Fluxo de Verificação
1. Usuário registra conta
2. Sistema envia código SMS
3. Usuário digita código
4. Sistema valida e ativa conta
5. Redirecionamento para configuração

### Configurações
```python
# settings.py
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_SID = os.getenv('TWILIO_VERIFY_SERVICE_SID')
```

---

## 💰 Sistema de Planos e Preços

### Modelo de Planos
```python
class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_users = models.IntegerField()
    max_customers = models.IntegerField()
    max_products = models.IntegerField()
    max_projects = models.IntegerField()
    stl_security = models.BooleanField(default=False)
    is_trial = models.BooleanField(default=False)
    trial_days = models.IntegerField(default=15)
    is_active = models.BooleanField(default=True)
```

### Planos Disponíveis
1. **Trial** (Gratuito)
   - 15 dias
   - 1 usuário
   - 5 clientes
   - 10 produtos
   - 2 projetos
   - Sem segurança STL

2. **Basic** (Pago)
   - R$ 79,90/mês ou R$ 799,90/ano
   - 5 usuários
   - 50 clientes
   - 100 produtos
   - 20 projetos
   - Sem segurança STL

3. **Premium** (Pago)
   - R$ 119,90/mês ou R$ 1.199,90/ano
   - 20 usuários
   - 200 clientes
   - 500 produtos
   - 100 projetos
   - **Com segurança STL**

### Sistema Multi-Moeda
- ✅ **BRL** (Brasil) - R$
- ✅ **USD** (EUA e outros) - $
- ✅ **EUR** (Europa) - €

### Geolocalização
```python
class GeolocationService:
    @staticmethod
    def get_client_ip(request)
    @staticmethod
    def get_country_by_ip(ip)
    @staticmethod
    def get_currency_by_country(country_code)
    @staticmethod
    def detect_user_currency(request)
```

### Mapeamento País → Moeda
- **BR** → BRL (Real)
- **US, CA, GB** → USD (Dólar)
- **DE, FR, IT, ES, NL, BE, AT, PT, IE, FI, SE, DK, NO, CH** → EUR (Euro)
- **Outros** → USD (Dólar)

---

## 🏢 Gestão de Empresas

### Modelo de Empresa
```python
class Company(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='company_logos/')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Funcionalidades
- ✅ Criação de empresa após verificação SMS
- ✅ Upload de logo
- ✅ Configuração de dados básicos
- ✅ Associação com usuário proprietário

---

## 👥 Gestão de Usuários

### Modelo de Usuário
```python
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, blank=True)
    verification_expires_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
```

### Funcionalidades
- ✅ Registro com validação única
- ✅ Verificação por SMS
- ✅ Perfil de usuário
- ✅ Gestão de dados pessoais
- ✅ Associação com país

---

## 💳 Sistema de Assinaturas

### Modelo de Assinatura
```python
class Subscription(models.Model):
    STATUS_CHOICES = [
        ('trial', 'Trial'),
        ('active', 'Ativa'),
        ('cancelled', 'Cancelada'),
        ('expired', 'Expirada'),
    ]
    
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Mensal'),
        ('yearly', 'Anual'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    next_billing_date = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)
```

### Funcionalidades
- ✅ Assinatura automática no registro
- ✅ Contador de dias restantes
- ✅ Renovação automática
- ✅ Gestão de ciclos de cobrança
- ✅ Status de assinatura

---

## 🎨 Interface do Usuário

### Header/Navbar
- ✅ Seletor de idioma
- ✅ Informações do plano atual
- ✅ Contador de dias restantes (trial)
- ✅ Menu de usuário
- ✅ Link para gestão de assinatura

### Página Inicial
- ✅ Exibição de planos comerciais
- ✅ Preços dinâmicos por moeda
- ✅ Toggle mensal/anual
- ✅ Descrições traduzidas
- ✅ Botões de ação

### Formulários
- ✅ Validação em tempo real
- ✅ Mensagens de erro traduzidas
- ✅ Campos obrigatórios marcados
- ✅ Upload de arquivos
- ✅ Seleção de países com bandeiras

---

## 🗄️ Banco de Dados

### Modelos Principais
- **User** - Usuários do sistema
- **Company** - Empresas
- **Plan** - Planos de assinatura
- **PlanPrice** - Preços por moeda
- **Subscription** - Assinaturas ativas
- **LoginAttempt** - Tentativas de login
- **Country** - Países disponíveis

### Migrações
- ✅ Estrutura inicial
- ✅ Campos de verificação SMS
- ✅ Sistema de planos
- ✅ Preços multi-moeda
- ✅ Assinaturas
- ✅ Campos traduzidos

---

## 🔧 Configurações Técnicas

### Dependências Principais
```
Django==5.2.4
Pillow (upload de imagens)
python-dotenv (variáveis de ambiente)
requests (geolocalização)
```

### Variáveis de Ambiente
```bash
# .env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True

# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_VERIFY_SERVICE_SID=your_verify_service_sid
```

### Configurações Django
```python
# settings.py
LANGUAGES = [
    ('pt', 'Português'),
    ('en', 'English'),
    ('es', 'Español'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    # ... outros middlewares
]
```

---

## 🧪 Testes e Validações

### Funcionalidades Testadas
- ✅ Registro de usuário
- ✅ Verificação SMS
- ✅ Login e logout
- ✅ Troca de idioma
- ✅ Sistema de segurança
- ✅ Geolocalização
- ✅ Preços multi-moeda
- ✅ Configuração de empresa
- ✅ Gestão de planos

### Cenários Validados
- ✅ Usuário brasileiro vê preços em BRL
- ✅ Usuário americano vê preços em USD
- ✅ Usuário europeu vê preços em EUR
- ✅ Preços não mudam com troca de idioma
- ✅ Sistema de bloqueio funciona
- ✅ Verificação SMS completa
- ✅ Traduções funcionam corretamente

---

## 🚀 Deploy e Produção

### Requisitos de Produção
- ✅ Configuração de HTTPS
- ✅ Variáveis de ambiente seguras
- ✅ Banco de dados PostgreSQL
- ✅ Servidor WSGI/ASGI
- ✅ CDN para arquivos estáticos
- ✅ Backup automático

### Monitoramento
- ✅ Logs de tentativas de login
- ✅ Logs de verificação SMS
- ✅ Logs de criação de conta
- ✅ Logs de mudança de plano

---

## 📋 Próximos Passos

### Funcionalidades Futuras
- [ ] Sistema de pagamento (PayPal/Stripe)
- [ ] Notificações de expiração
- [ ] Backup automático
- [ ] API REST
- [ ] Autenticação 2FA
- [ ] Logs de auditoria
- [ ] Relatórios avançados

### Melhorias Planejadas
- [ ] Otimização de performance
- [ ] Cache Redis
- [ ] Testes automatizados
- [ ] Documentação da API
- [ ] Dashboard administrativo

---

## 📞 Suporte

### Contatos
- **Desenvolvedor**: Rodrigo Silva
- **E-mail**: rodrigoa_silva@hotmail.com
- **Projeto**: ForgeLock Web Platform

### Repositório
- **Localização**: C:\ProjetoForgeLock
- **Versão**: 1.0.0
- **Última atualização**: 30/07/2025

---

*Documentação gerada automaticamente em 30/07/2025* 