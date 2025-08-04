from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required


def subscription_required(view_func):
    """
    Decorator que verifica se o usuário tem uma assinatura ativa
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verificar se tem assinatura ativa
        subscription = request.user.subscriptions.filter(status__in=['trial', 'active']).first()
        
        if not subscription:
            messages.error(request, _('Você precisa de uma assinatura ativa para acessar esta funcionalidade.'))
            return redirect('subscription')
        
        # Adicionar subscription ao request para uso na view
        request.user_subscription = subscription
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def full_access_required(view_func):
    """
    Decorator que verifica se o usuário tem acesso completo (não está em carência)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verificar se tem assinatura ativa
        subscription = request.user.subscriptions.filter(status__in=['trial', 'active']).first()
        
        if not subscription:
            messages.error(request, _('Você precisa de uma assinatura ativa para acessar esta funcionalidade.'))
            return redirect('subscription')
        
        # Verificar se está em período de carência
        if subscription.is_in_grace_period():
            messages.warning(request, _('Sua assinatura expirou. Você está no período de carência e pode apenas visualizar dados.'))
            return redirect('subscription')
        
        # Adicionar subscription ao request para uso na view
        request.user_subscription = subscription
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def read_only_access(view_func):
    """
    Decorator que permite acesso apenas para visualização (inclui período de carência)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verificar se tem assinatura ativa ou está em carência
        subscription = request.user.subscriptions.filter(status__in=['trial', 'active', 'grace_period']).first()
        
        if not subscription:
            messages.error(request, _('Você precisa de uma assinatura ativa para acessar esta funcionalidade.'))
            return redirect('subscription')
        
        # Adicionar subscription ao request para uso na view
        request.user_subscription = subscription
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def check_subscription_status(view_func):
    """
    Decorator que verifica o status da assinatura e adiciona informações ao contexto
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Buscar assinatura (incluindo expiradas para mostrar status)
            subscription = request.user.subscriptions.filter(status__in=['trial', 'active', 'grace_period', 'expired']).first()
            
            if subscription:
                # Adicionar informações ao request
                request.user_subscription = subscription
                request.subscription_status = subscription.status
                request.days_remaining = subscription.get_days_remaining()
                request.grace_period_days = subscription.get_grace_period_days_remaining()
                request.can_edit = subscription.can_access_full_features()
                request.can_view = subscription.can_access_read_only()
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view 