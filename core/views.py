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
from .services import VerificationService
from .models import User, Country, Plan, Account
from django.utils import translation

verification_service = VerificationService()


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
                defaults={'duration_days': 15, 'price': 0}
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
                del request.session['user_id']
                return redirect('dashboard')
            else:
                if verification_service.is_code_expired(user):
                    messages.error(request, _('Código expirado. Um novo código foi enviado.'))
                    verification_service.send_verification_code(user)
                else:
                    messages.error(request, _('Código inválido. Tente novamente.'))
    else:
        form = SMSVerificationForm()
    
    return render(request, 'core/verify_sms.html', {
        'form': form,
        'user': user,
        'expiry_minutes': verification_service.expiry_minutes
    })


def resend_sms(request):
    """Reenvia código SMS"""
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
    
    return redirect('verify_sms')


def user_login(request):
    """Login de usuário"""
    # Forçar ativação do idioma baseado na sessão
    session_language = request.session.get('django_language')
    if session_language:
        translation.activate(session_language)
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                login(request, user)
                messages.success(request, _('Login realizado com sucesso!'))
                return redirect('dashboard')
            else:
                messages.error(request, _('Conta não verificada. Verifique seu telefone.'))
                request.session['user_id'] = user.id
                return redirect('verify_sms')
    else:
        # Criar formulário APÓS ativar o idioma
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
    """API para obter DDI do país"""
    try:
        country = Country.objects.get(id=country_id)
        return JsonResponse({'ddi': country.ddi})
    except Country.DoesNotExist:
        return JsonResponse({'error': 'País não encontrado'}, status=404)
