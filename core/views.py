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

verification_service = VerificationService()


def home(request):
    """Página inicial"""
    return render(request, 'core/home.html')


def user_register(request):
    """Registro de usuário"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            
            # Definir trial de 15 dias
            user.trial_expires = timezone.now() + timedelta(days=15)
            user.save()
            
            # Criar plano trial
            trial_plan, created = Plan.objects.get_or_create(
                name="Trial",
                defaults={
                    'description': "Plano trial de 15 dias",
                    'price': 0,
                    'max_users': 1,
                    'max_customers': 10,
                    'max_products': 5,
                    'max_projects': 3,
                    'has_stl_security': False,
                    'is_active': True
                }
            )
            
            # Criar account
            Account.objects.create(user=user, plan=trial_plan)
            
            # Enviar código SMS
            if verification_service.send_verification_code(user):
                messages.success(request, _('Conta criada com sucesso! Verifique seu telefone para o código de confirmação.'))
                request.session['user_id'] = user.id
                return redirect('verify_sms')
            else:
                messages.error(request, _('Erro ao enviar código de verificação. Tente novamente.'))
                user.delete()
                return redirect('register')
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
        form = CompanyForm()
    
    return render(request, 'core/company_setup.html', {'form': form})


def change_language(request):
    """Muda o idioma da aplicação"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            request.session['django_language'] = language
            request.session.modified = True
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def get_country_ddi(request, country_id):
    """API para obter DDI do país"""
    try:
        country = Country.objects.get(id=country_id)
        return JsonResponse({'ddi': country.ddi})
    except Country.DoesNotExist:
        return JsonResponse({'error': 'País não encontrado'}, status=404)
