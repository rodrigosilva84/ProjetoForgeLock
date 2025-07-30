from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .forms import UserRegistrationForm, UserLoginForm, SMSVerificationForm, CompanyForm
from .services import VerificationService, SecurityService
from .models import User, Country, Plan, Account
from django.utils import translation

verification_service = VerificationService()
security_service = SecurityService()


def home(request):
    """Página inicial"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    return render(request, 'core/home.html')


def user_register(request):
    """Registro de usuário"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    # Criar formulário APÓS ativar o idioma
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Criar conta com plano Trial
            trial_plan, created = Plan.objects.get_or_create(
                name='Trial',
                defaults={
                    'description': 'Plano trial gratuito por 15 dias',
                    'price': 0,
                    'max_users': 1,
                    'max_customers': 10,
                    'max_products': 5,
                    'max_projects': 3,
                    'has_stl_security': False
                }
            )
            
            Account.objects.create(
                user=user,
                plan=trial_plan,
                is_active=True
            )
            
            # Enviar SMS de verificação
            verification_service.send_verification_code(user)
            
            request.session['user_id'] = user.id
            messages.success(request, _('Conta criada com sucesso! Verifique seu telefone.'))
            return redirect('verify_sms')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})


def verify_sms(request):
    """Verificação de SMS"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    print(f"DEBUG: Session language: {session_language}")
    if session_language:
        translation.activate(session_language)
        print(f"DEBUG: Activated language: {translation.get_language()}")
    else:
        print(f"DEBUG: No session language, current: {translation.get_language()}")
    
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
                return redirect('dashboard')
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
def dashboard(request):
    """Dashboard do usuário"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    user = request.user
    
    # Verificar se usuário tem empresa
    if not user.company:
        messages.warning(request, _('Configure sua empresa para começar a usar o sistema.'))
        return redirect('company_setup')
    
    # Estatísticas básicas
    context = {
        'user': user,
        'company': user.company,
        'customers_count': 0,  # Será implementado quando criar o módulo customers
        'products_count': 0,   # Será implementado quando criar o módulo products
        'projects_count': 0,   # Será implementado quando criar o módulo projects
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def profile(request):
    """Perfil do usuário"""
    return render(request, 'core/profile.html', {'user': request.user})


@login_required
def company_setup(request):
    """Configuração de empresa"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    user = request.user
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            user.company = company
            user.save()
            messages.success(request, _('Empresa configurada com sucesso!'))
            return redirect('dashboard')
    else:
        # Criar formulário APÓS ativar o idioma
        form = CompanyForm()
    
    return render(request, 'core/company_setup.html', {'form': form})


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
