from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .forms import UserRegistrationForm, UserLoginForm, SMSVerificationForm, CompanyForm, UserProfileForm
from .services import VerificationService, SecurityService
from .models import User, Country, Plan, Account, PlanPrice
from django.utils import translation
from .decorators import subscription_required, full_access_required, read_only_access, check_subscription_status

verification_service = VerificationService()
security_service = SecurityService()


def test_view(request):
    """View de teste simples"""
    return HttpResponse("Teste funcionando!")


def get_user_currency(request):
    """Detecta a moeda baseada na localização do usuário"""
    from .services import GeolocationService
    return GeolocationService.detect_user_currency(request)

def get_currency_symbol(currency_code):
    """Converte código da moeda para símbolo"""
    currency_symbols = {
        'BRL': 'R$',
        'USD': '$',
        'EUR': '€'
    }
    return currency_symbols.get(currency_code, currency_code)


def home(request):
    """Página inicial"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language') if hasattr(request, 'session') else None
    if session_language:
        translation.activate(session_language)
    
    # Buscar planos ativos (excluir Admin, Trial e Vitalicio)
    plans = Plan.objects.filter(is_active=True, is_trial=False).exclude(name__iexact='admin').exclude(name__iexact='vitalicio').order_by('name')
    
    # Detectar moeda do usuário
    user_currency = get_user_currency(request)
    user_currency_symbol = get_currency_symbol(user_currency)
    
    # Configurar moeda para cada plano
    for plan in plans:
        plan._user_currency = user_currency
    
    return render(request, 'core/home.html', {
        'plans': plans,
        'user_currency': user_currency,
        'user_currency_symbol': user_currency_symbol
    })


def user_register(request, plan_id=None):
    """Registro de usuário"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    # Buscar plano se especificado
    selected_plan = None
    if plan_id:
        try:
            selected_plan = Plan.objects.get(id=plan_id, is_active=True)
        except Plan.DoesNotExist:
            messages.error(request, _('Plano não encontrado.'))
            return redirect('home')
    
    # Criar formulário APÓS ativar o idioma
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Usar plano escolhido pelo usuário ou Basic como padrão
            if selected_plan:
                plan_to_use = selected_plan
            else:
                plan_to_use = Plan.objects.filter(name='Basic', is_active=True).first()
                if not plan_to_use:
                    messages.error(request, _('Plano Basic não encontrado. Contate o suporte.'))
                    return redirect('home')
            
            # Criar conta
            account = Account.objects.create(
                user=user,
                plan=plan_to_use,
                is_active=True
            )
            
            # Criar assinatura trial (15 dias)
            from .models import Subscription
            from django.utils import timezone
            from datetime import timedelta
            
            trial_end_date = timezone.now() + timedelta(days=15)
            Subscription.objects.create(
                user=user,
                plan=plan_to_use,
                status='trial',
                billing_cycle='monthly',
                start_date=timezone.now(),
                end_date=trial_end_date
            )
            

            
            # Enviar SMS de verificação
            verification_service.send_verification_code(user)
            
            request.session['user_id'] = user.id
            messages.success(request, _('Conta criada com sucesso! Verifique seu telefone.'))
            return redirect('verify_sms')
    else:
        form = UserRegistrationForm()
    
    # Se não há plano selecionado, usar Basic como padrão
    if not selected_plan:
        selected_plan = Plan.objects.filter(name='Basic', is_active=True).first()
    
    # Garantir que temos um plano válido
    if not selected_plan:
        messages.error(request, _('Nenhum plano disponível. Contate o suporte.'))
        return redirect('home')
    
    return render(request, 'core/register.html', {
        'form': form,
        'plan': selected_plan,
        'is_plan_selected': plan_id is not None
    })


def user_register_with_plan(request, plan_id):
    """Registro de usuário com plano específico"""
    return user_register(request, plan_id)


def verify_sms(request):
    """Verificação de SMS"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, _('Sessão expirada. Faça o registro novamente.'))
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, _('Usuário não encontrado.'))
        return redirect('register')
    
    if request.method == 'POST':
        form = SMSVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['verification_code']
            
            if verification_service.verify_code(user, code):
                login(request, user)
                messages.success(request, _('Conta verificada com sucesso! Bem-vindo ao ForgeLock.'))
                request.session.pop('user_id', None)
                return redirect('profile_setup')
            else:
                if verification_service.is_code_expired(user):
                    messages.error(request, _('Código expirado. Um novo código foi enviado.'))
                    verification_service.send_verification_code(user)
                else:
                    messages.error(request, _('Código inválido. Tente novamente.'))
    else:
        # Criar formulário APÓS ativar o idioma
        form = SMSVerificationForm()
    
    return render(request, 'core/verify_sms.html', {
        'form': form,
        'user': user,
        'expiry_minutes': verification_service.expiry_minutes
    })


def resend_sms(request):
    """Reenvia código SMS"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                if verification_service.send_verification_code(user):
                    messages.success(request, _('Novo código enviado com sucesso!'))
                else:
                    messages.error(request, _('Erro ao enviar código. Tente novamente.'))
            except User.DoesNotExist:
                messages.error(request, _('Usuário não encontrado.'))
                request.session.pop('user_id', None)
        else:
            messages.error(request, _('Sessão expirada. Faça o registro novamente.'))
            return redirect('register')
    
    return redirect('verify_sms')


def get_client_ip(request):
    """Obtém o IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def user_login(request):
    """Login de usuário - VERSÃO SIMPLIFICADA"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Verificar se o login deve ser bloqueado
            should_block, block_message = security_service.should_block_login(username_or_email, ip_address)
            if should_block:
                messages.error(request, _(block_message))
                return render(request, 'core/login.html', {'form': form})
            
            # Tentar autenticar o usuário
            user = authenticate(request, username=username_or_email, password=password)
            
            if user is not None:
                # Login bem-sucedido
                if user.is_verified:
                    login(request, user)
                    security_service.record_login_attempt(username_or_email, ip_address, True, user_agent)
                    
                    # Limpar tentativas antigas deste usuário após login bem-sucedido
                    from .models import LoginAttempt
                    LoginAttempt.objects.filter(username=username_or_email).delete()
                    
                    messages.success(request, _('Login realizado com sucesso!'))
                    return redirect('dashboard')
                else:
                    # Usuário não verificado
                    security_service.record_login_attempt(username_or_email, ip_address, False, user_agent)
                    messages.error(request, _('Conta não verificada. Verifique seu telefone.'))
                    request.session['user_id'] = user.id
                    return redirect('verify_sms')
            else:
                # Login falhou - verificar se usuário existe
                try:
                    if '@' in username_or_email:
                        user = User.objects.get(email=username_or_email)
                    else:
                        user = User.objects.get(username=username_or_email)
                    
                    # Usuário existe, senha incorreta
                    security_service.record_login_attempt(username_or_email, ip_address, False, user_agent)
                    
                    failed_attempts = security_service.get_failed_attempts_count(username_or_email, ip_address)
                    remaining_attempts = security_service.MAX_ATTEMPTS - failed_attempts
                    
                    if remaining_attempts > 0:
                        messages.error(request, _('Senha incorreta. Tentativas restantes: {}').format(remaining_attempts))
                    else:
                        messages.error(request, _('Senha incorreta.'))
                        
                except User.DoesNotExist:
                    # Usuário não existe
                    messages.error(request, _('Usuário não encontrado. Verifique o nome de usuário ou email.'))
    else:
        form = UserLoginForm()
    
    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    """Logout de usuário"""
    logout(request)
    messages.success(request, _('Logout realizado com sucesso!'))
    return redirect('home')


@login_required
@check_subscription_status
def dashboard(request):
    """Dashboard do usuário"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    user = request.user
    
    # Verificar se usuário tem empresa
    primary_company = user.get_primary_company()
    if not primary_company:
        messages.warning(request, _('Configure sua empresa para começar a usar o sistema.'))
        return redirect('company_setup')
    
    # Estatísticas da empresa do usuário
    company = primary_company
    company_members = User.objects.filter(companies=company).count()
    
    # Estatísticas do plano atual
    current_plan = user.account.plan if hasattr(user, 'account') and user.account else None
    plan_name = current_plan.name if current_plan else _('Nenhum plano')
    
    # Verificar se o usuário é admin (superuser ou staff)
    is_admin = user.is_superuser or user.is_staff
    
    # Calcular contagens reais de clientes e produtos
    from customers.models import Customer
    from products.models import Product
    
    customers_count = Customer.objects.filter(company=company).count()
    products_count = Product.objects.filter(company=company).count()
    projects_count = 0  # Placeholder até o modelo Project ser implementado
    
    # Estatísticas baseadas no tipo de usuário
    if is_admin:
        # Para admins: mostrar estatísticas globais
        from .models import Company, Plan, Country
        
        total_users = User.objects.count()
        verified_users = User.objects.filter(is_verified=True).count()
        unverified_users = User.objects.filter(is_verified=False).count()
        total_companies = Company.objects.count()
        total_plans = Plan.objects.count()
        total_countries = Country.objects.count()
        
        context = {
            'user': user,
            'company': company,
            'is_admin': True,
            
            # Estatísticas globais (apenas para admin)
            'total_users': total_users,
            'verified_users': verified_users,
            'unverified_users': unverified_users,
            'total_companies': total_companies,
            'total_plans': total_plans,
            'total_countries': total_countries,
            
            # Estatísticas pessoais
            'company_members': company_members,
            'current_plan': current_plan,
            'plan_name': plan_name,
            
            # Informações da assinatura
            'subscription_status': getattr(request, 'subscription_status', None),
            'days_remaining': getattr(request, 'days_remaining', 0),
            'grace_period_days': getattr(request, 'grace_period_days', 0),
            'can_edit': getattr(request, 'can_edit', True),
            'can_view': getattr(request, 'can_view', True),
            
            # Contagens reais dos módulos
            'customers_count': customers_count,
            'products_count': products_count,
            'projects_count': projects_count,
        }
    else:
        # Para usuários normais: mostrar apenas informações pessoais
        context = {
            'user': user,
            'company': company,
            'is_admin': False,
            
            # Estatísticas pessoais
            'company_members': company_members,
            'current_plan': current_plan,
            'plan_name': plan_name,
            
            # Informações da assinatura
            'subscription_status': getattr(request, 'subscription_status', None),
            'days_remaining': getattr(request, 'days_remaining', 0),
            'grace_period_days': getattr(request, 'grace_period_days', 0),
            'can_edit': getattr(request, 'can_edit', True),
            'can_view': getattr(request, 'can_view', True),
            
            # Contagens reais dos módulos
            'customers_count': customers_count,
            'products_count': products_count,
            'projects_count': projects_count,
        }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def profile_setup(request):
    """Setup inicial do perfil do usuário"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    user = request.user
    
    # Verificar se é primeiro acesso usando o campo booleano
    is_first_access = user.is_first_access
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        # Se é primeiro acesso e clicou em "Avançar", apenas navegar
        if is_first_access and request.POST.get('action') == 'avancar':
            messages.success(request, _('Perfil atualizado com sucesso!'))
            return redirect('company_setup')
        
        # Se chegou aqui, é para salvar os dados
        if form.is_valid():
            user = form.save()
            messages.success(request, _('Perfil atualizado com sucesso!'))
            
            # Sempre permanecer na mesma página após salvar
            return redirect('profile_setup')
        else:
            # Se houver erros, mostrar mensagem
            messages.error(request, _('Por favor, corrija os erros no formulário.'))
    else:
        # Criar formulário APÓS ativar o idioma
        form = UserProfileForm(instance=user)
    
    return render(request, 'core/profile_setup.html', {
        'form': form, 
        'user': user,
        'is_first_access': is_first_access
    })


@login_required
def profile(request):
    """Perfil do usuário"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    return render(request, 'core/profile.html', {'user': request.user})


@login_required
def subscription(request):
    """Página de assinatura/plano"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    return render(request, 'core/subscription.html', {'user': request.user})


@login_required
@read_only_access
def products(request):
    """Página de produtos"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    return render(request, 'core/products.html', {'user': request.user})


@login_required
@read_only_access
def projects(request):
    """Página de projetos"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    return render(request, 'core/projects.html', {'user': request.user})


@login_required
def company_setup(request):
    """Configuração de empresa"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    user = request.user
    
    # Verificar se é primeiro acesso usando o campo booleano
    is_first_access = user.is_first_access
    
    # Verificar se o usuário já tem uma empresa
    existing_company = user.get_primary_company()
    
    if request.method == 'POST':
        # Se já existe uma empresa, usar a instância existente
        if existing_company:
            form = CompanyForm(request.POST, request.FILES, instance=existing_company, user=user)
        else:
            form = CompanyForm(request.POST, request.FILES, user=user)
            
        # Se é primeiro acesso e clicou em "Avançar", apenas navegar
        if is_first_access and request.POST.get('action') == 'avancar':
            user.is_first_access = False
            user.save()
            messages.success(request, _('Empresa configurada com sucesso!'))
            return redirect('dashboard')
        
        # Se chegou aqui, é para salvar os dados
        if form.is_valid():
            company = form.save()
            # Só associar a empresa ao usuário se ela não existia antes
            if not existing_company:
                from .models import UserCompany
                UserCompany.objects.create(
                    user=user,
                    company=company,
                    role='owner',
                    is_active=True
                )
            
            messages.success(request, _('Empresa configurada com sucesso!'))
            
            # Sempre permanecer na mesma página após salvar
            return redirect('company_setup')
        else:
            # Debug: mostrar erros do formulário
            print("Erros do formulário:", form.errors)
            for field_name, errors in form.errors.items():
                print(f"Campo {field_name}: {errors}")
    else:
        # Criar formulário APÓS ativar o idioma, passando o usuário e a instância existente
        if existing_company:
            form = CompanyForm(instance=existing_company, user=user)
        else:
            form = CompanyForm(user=user)
    
    return render(request, 'core/company_setup.html', {
        'form': form, 
        'user': user,
        'is_first_access': is_first_access
    })


def change_language(request):
    """Muda o idioma da aplicação"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language and language in ['pt', 'en', 'es']:
            # Ativar o idioma imediatamente
            translation.activate(language)
            request.session['django_language'] = language
            request.session.modified = True
        else:
            pass # No debug print for invalid language
    
    referer = request.META.get('HTTP_REFERER', 'home')
    return redirect(referer)


def get_country_ddi(request, country_id):
    """Retorna o DDI de um país"""
    try:
        country = Country.objects.get(id=country_id)
        return JsonResponse({'ddi': country.ddi})
    except Country.DoesNotExist:
        return JsonResponse({'error': 'País não encontrado'}, status=404)


def password_reset_request(request):
    """Solicitação de recuperação de senha"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Aqui você implementaria o envio do email de recuperação
            # Por enquanto, vamos apenas mostrar uma mensagem de sucesso
            messages.success(request, _('Email de recuperação enviado com sucesso!'))
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, _('Email não encontrado no sistema.'))
    
    return render(request, 'core/password_reset_request.html')


def password_reset_confirm(request, token):
    """Confirmação de recuperação de senha"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            # Aqui você implementaria a validação do token
            # Por enquanto, vamos apenas mostrar uma mensagem de sucesso
            messages.success(request, _('Senha alterada com sucesso!'))
            return redirect('login')
        else:
            messages.error(request, _('As senhas não coincidem.'))
    
    return render(request, 'core/password_reset_confirm.html')


def unblock_ip(request):
    """View temporária para desbloquear IP (apenas para desenvolvimento)"""
    if request.method == 'POST':
        ip_address = get_client_ip(request)
        security_service.unblock_ip(ip_address)
        messages.success(request, f'IP {ip_address} desbloqueado!')
    return redirect('login')


def clear_all_blocks(request):
    """View temporária para limpar todos os bloqueios (apenas para desenvolvimento)"""
    if request.method == 'POST':
        # Limpar cache de bloqueios
        from django.core.cache import cache
        cache.clear()
        messages.success(request, 'Todos os bloqueios foram removidos!')
    return redirect('login')


def clear_all_login_attempts(request):
    """View temporária para limpar todas as tentativas de login (apenas para desenvolvimento)"""
    if request.method == 'POST':
        from .models import LoginAttempt
        from django.core.cache import cache
        
        # Limpar todas as tentativas de login
        LoginAttempt.objects.all().delete()
        
        # Limpar cache
        cache.clear()
        
        messages.success(request, 'Todas as tentativas de login foram removidas!')
    return redirect('login')


def force_unblock(request):
    """View para forçar desbloqueio imediato (apenas para desenvolvimento)"""
    if request.method == 'POST':
        from django.core.cache import cache
        from .models import LoginAttempt
        
        # Limpar cache
        cache.clear()
        
        # Limpar tentativas antigas
        cutoff_time = timezone.now() - timedelta(minutes=15)
        LoginAttempt.objects.filter(timestamp__lt=cutoff_time).delete()
        
        messages.success(request, 'Sistema desbloqueado!')
    return redirect('login')


def clear_attempts(request):
    """Limpa todas as tentativas de login"""
    from .models import LoginAttempt
    LoginAttempt.objects.all().delete()
    messages.success(request, 'Tentativas limpas!')
    return redirect('login')


def test_address_autocomplete(request):
    """View para testar a automação de endereço"""
    return render(request, 'test_address_autocomplete.html')
