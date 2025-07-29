import os
import random
import string
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import logging
from django.core.cache import cache
from .models import LoginAttempt

logger = logging.getLogger(__name__)


class SMSService:
    """Serviço para envio de SMS usando Twilio"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        
    def send_sms(self, to_number, message):
        """Envia SMS usando Twilio"""
        if settings.SMS_DEVELOPMENT_MODE:
            # Modo desenvolvimento - simula envio
            logger.info(f"SMS SIMULADO para {to_number}: {message}")
            return self._send_email_fallback(to_number, message)
        
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            message = client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            logger.info(f"SMS enviado com sucesso: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar SMS: {e}")
            return self._send_email_fallback(to_number, message)
    
    def _send_email_fallback(self, to_number, message):
        """Fallback para email em caso de erro no SMS"""
        try:
            subject = "Código de Verificação ForgeLock"
            email_message = f"""
            Código de verificação: {message}
            
            Este é um código de verificação para sua conta ForgeLock.
            Se você não solicitou este código, ignore este email.
            """
            
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [f"{to_number}@example.com"],  # Email fictício
                fail_silently=False,
            )
            logger.info(f"Email de fallback enviado para {to_number}")
            return True
            
        except Exception as e:
            logger.error(f"Erro no fallback de email: {e}")
            return False


class VerificationService:
    """Serviço para verificação SMS"""
    
    def generate_verification_code(self):
        """Gera código de verificação de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    def send_verification_code(self, user):
        """Envia código de verificação via SMS"""
        code = self.generate_verification_code()
        user.verification_code = code
        user.verification_expires_at = timezone.now() + timedelta(minutes=10)
        user.save()
        
        # Aqui você implementaria o envio real do SMS
        # Por enquanto, apenas simulamos
        print(f"Código de verificação para {user.phone_number}: {code}")
    
    def verify_code(self, user, code):
        """Verifica código de verificação"""
        if user.verification_code == code and not self.is_code_expired(user):
            user.is_verified = True
            user.verification_code = None
            user.verification_expires_at = None
            user.save()
            return True
        return False
    
    def is_code_expired(self, user):
        """Verifica se o código expirou"""
        return user.verification_expires_at and user.verification_expires_at < timezone.now()


class SecurityService:
    """Serviço para segurança do login - COM LIMPEZA AUTOMÁTICA"""
    
    MAX_ATTEMPTS = 5  # Máximo de tentativas
    CLEANUP_MINUTES = 3  # Limpa tentativas após 3 minutos
    
    def record_login_attempt(self, username, ip_address, success, user_agent=''):
        """Registra uma tentativa de login"""
        LoginAttempt.objects.create(
            username=username,
            ip_address=ip_address,
            success=success,
            user_agent=user_agent
        )
    
    def cleanup_old_attempts(self):
        """Limpa tentativas antigas automaticamente"""
        cutoff_time = timezone.now() - timedelta(minutes=self.CLEANUP_MINUTES)
        deleted_count = LoginAttempt.objects.filter(timestamp__lt=cutoff_time).delete()[0]
        if deleted_count > 0:
            print(f"DEBUG: Limpou {deleted_count} tentativas antigas")
    
    def get_failed_attempts_count(self, username, ip_address):
        """Conta tentativas falhadas - COM LIMPEZA AUTOMÁTICA"""
        # Limpar tentativas antigas primeiro
        self.cleanup_old_attempts()
        
        return LoginAttempt.objects.filter(
            username=username,
            ip_address=ip_address,
            success=False
        ).count()
    
    def should_block_login(self, username, ip_address):
        """Determina se o login deve ser bloqueado - COM LIMPEZA AUTOMÁTICA"""
        try:
            from .models import User
            if '@' in username:
                user_exists = User.objects.filter(email=username).exists()
            else:
                user_exists = User.objects.filter(username=username).exists()
            
            # Se usuário não existe, não bloquear
            if not user_exists:
                print(f"DEBUG: Usuário {username} não existe, não bloqueando")
                return False, None
            
            # Se usuário existe, verificar tentativas (com limpeza automática)
            failed_attempts = self.get_failed_attempts_count(username, ip_address)
            print(f"DEBUG: Usuário {username} - Tentativas falhadas: {failed_attempts}")
            
            if failed_attempts >= self.MAX_ATTEMPTS:
                print(f"DEBUG: Usuário {username} bloqueado - {failed_attempts} tentativas")
                return True, f"Muitas tentativas falhadas. Tente novamente em {self.CLEANUP_MINUTES} minutos."
            
        except Exception as e:
            print(f"DEBUG: Erro ao verificar bloqueio: {e}")
            pass
        
        return False, None