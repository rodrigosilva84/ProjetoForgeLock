"""
Sistema de Notificações - ForgeLock
Gerencia envio de emails e SMS para notificações de assinatura
"""

import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .services import VerificationService


class NotificationService:
    """Serviço para envio de notificações"""
    
    def __init__(self):
        self.verification_service = VerificationService()
    
    def send_subscription_notification(self, subscription, notification_type):
        """
        Envia notificação baseada no tipo
        
        Args:
            subscription: Objeto Subscription
            notification_type: 'expiring_soon', 'expired', 'grace_period', 'blocked'
        """
        user = subscription.user
        
        if notification_type == 'expiring_soon':
            return self._send_expiring_soon_notification(subscription)
        elif notification_type == 'expired':
            return self._send_expired_notification(subscription)
        elif notification_type == 'grace_period':
            return self._send_grace_period_notification(subscription)
        elif notification_type == 'blocked':
            return self._send_blocked_notification(subscription)
        else:
            return False
    
    def _send_expiring_soon_notification(self, subscription):
        """Notificação 10 dias antes do vencimento"""
        user = subscription.user
        days_remaining = subscription.get_days_remaining()
        
        # Email
        subject = _('Sua assinatura vence em {} dias').format(days_remaining)
        message = self._get_email_template('expiring_soon', {
            'user': user,
            'subscription': subscription,
            'days_remaining': days_remaining,
            'plan_name': subscription.plan.get_localized_name()
        })
        
        email_sent = self._send_email(user.email, subject, message)
        
        # SMS (opcional)
        sms_sent = False
        if hasattr(settings, 'TWILIO_ENABLED') and settings.TWILIO_ENABLED:
            sms_message = _('ForgeLock: Sua assinatura {} vence em {} dias. Renove agora!').format(
                subscription.plan.get_localized_name(), days_remaining
            )
            sms_sent = self._send_sms(user.phone_number, sms_message)
        
        return email_sent, sms_sent
    
    def _send_expired_notification(self, subscription):
        """Notificação no dia do vencimento"""
        user = subscription.user
        
        # Email
        subject = _('Sua assinatura expirou')
        message = self._get_email_template('expired', {
            'user': user,
            'subscription': subscription,
            'plan_name': subscription.plan.get_localized_name()
        })
        
        email_sent = self._send_email(user.email, subject, message)
        
        # SMS
        sms_sent = False
        if hasattr(settings, 'TWILIO_ENABLED') and settings.TWILIO_ENABLED:
            sms_message = _('ForgeLock: Sua assinatura {} expirou. Renove para continuar usando!').format(
                subscription.plan.get_localized_name()
            )
            sms_sent = self._send_sms(user.phone_number, sms_message)
        
        return email_sent, sms_sent
    
    def _send_grace_period_notification(self, subscription):
        """Notificação durante período de carência"""
        user = subscription.user
        grace_days = subscription.get_grace_period_days_remaining()
        
        # Email
        subject = _('Período de carência - {} dias restantes').format(grace_days)
        message = self._get_email_template('grace_period', {
            'user': user,
            'subscription': subscription,
            'grace_days': grace_days,
            'plan_name': subscription.plan.get_localized_name()
        })
        
        email_sent = self._send_email(user.email, subject, message)
        
        # SMS
        sms_sent = False
        if hasattr(settings, 'TWILIO_ENABLED') and settings.TWILIO_ENABLED:
            sms_message = _('ForgeLock: Você tem {} dias de carência. Renove sua assinatura {}!').format(
                grace_days, subscription.plan.get_localized_name()
            )
            sms_sent = self._send_sms(user.phone_number, sms_message)
        
        return email_sent, sms_sent
    
    def _send_blocked_notification(self, subscription):
        """Notificação quando acesso é bloqueado"""
        user = subscription.user
        
        # Email
        subject = _('Acesso bloqueado - Renove sua assinatura')
        message = self._get_email_template('blocked', {
            'user': user,
            'subscription': subscription,
            'plan_name': subscription.plan.get_localized_name()
        })
        
        email_sent = self._send_email(user.email, subject, message)
        
        # SMS
        sms_sent = False
        if hasattr(settings, 'TWILIO_ENABLED') and settings.TWILIO_ENABLED:
            sms_message = _('ForgeLock: Seu acesso foi bloqueado. Renove sua assinatura {} para continuar!').format(
                subscription.plan.get_localized_name()
            )
            sms_sent = self._send_sms(user.phone_number, sms_message)
        
        return email_sent, sms_sent
    
    def _send_email(self, to_email, subject, message):
        """Envia email"""
        try:
            # Em desenvolvimento, apenas log
            if settings.DEBUG:
                print(f"📧 EMAIL (DEV): {to_email}")
                print(f"   Assunto: {subject}")
                print(f"   Mensagem: {message[:100]}...")
                return True
            
            # Em produção, enviar email real
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            return False
    
    def _send_sms(self, phone_number, message):
        """Envia SMS"""
        try:
            # Em desenvolvimento, apenas log
            if settings.DEBUG:
                print(f"📱 SMS (DEV): {phone_number}")
                print(f"   Mensagem: {message}")
                return True
            
            # Em produção, usar Twilio
            if hasattr(settings, 'TWILIO_ENABLED') and settings.TWILIO_ENABLED:
                return self.verification_service.send_sms(phone_number, message)
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao enviar SMS: {e}")
            return False
    
    def _get_email_template(self, template_name, context):
        """Gera template de email"""
        try:
            # Template simples em texto
            if template_name == 'expiring_soon':
                return f"""
Olá {context['user'].first_name},

Sua assinatura {context['plan_name']} vence em {context['days_remaining']} dias.

Para continuar usando o ForgeLock sem interrupções, renove sua assinatura agora.

Acesse: {settings.SITE_URL}/subscription

Atenciosamente,
Equipe ForgeLock
                """
            
            elif template_name == 'expired':
                return f"""
Olá {context['user'].first_name},

Sua assinatura {context['plan_name']} expirou.

Você ainda tem 15 dias de período de carência para renovar sua assinatura.

Acesse: {settings.SITE_URL}/subscription

Atenciosamente,
Equipe ForgeLock
                """
            
            elif template_name == 'grace_period':
                return f"""
Olá {context['user'].first_name},

Você está no período de carência da sua assinatura {context['plan_name']}.

Restam {context['grace_days']} dias para renovar antes do bloqueio total.

Acesse: {settings.SITE_URL}/subscription

Atenciosamente,
Equipe ForgeLock
                """
            
            elif template_name == 'blocked':
                return f"""
Olá {context['user'].first_name},

Seu acesso ao ForgeLock foi bloqueado devido ao vencimento da assinatura {context['plan_name']}.

Para restaurar o acesso, renove sua assinatura agora.

Acesse: {settings.SITE_URL}/subscription

Atenciosamente,
Equipe ForgeLock
                """
            
            return "Notificação ForgeLock"
            
        except Exception as e:
            print(f"❌ Erro ao gerar template: {e}")
            return "Notificação ForgeLock"


# Instância global
notification_service = NotificationService() 