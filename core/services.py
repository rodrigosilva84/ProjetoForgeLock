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
import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

logger = logging.getLogger(__name__)


class TwilioService:
    """Serviço para envio de SMS usando Twilio"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        
    def send_sms(self, to_number, message):
        """Envia SMS usando Twilio"""
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            logger.warning("Credenciais Twilio não configuradas. Usando fallback.")
            return self._send_email_fallback(to_number, message)
        
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            message_obj = client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            logger.info(f"SMS enviado com sucesso: {message_obj.sid}")
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


class TwilioVerifyService:
    """Serviço para verificação usando Twilio Verify"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.verify_service_sid = settings.TWILIO_VERIFY_SERVICE_SID
        
    def send_verification(self, phone_number):
        """Envia código de verificação via Twilio Verify"""
        if not all([self.account_sid, self.auth_token, self.verify_service_sid]):
            logger.warning("Credenciais Twilio Verify não configuradas. Usando fallback.")
            return self._send_email_fallback(phone_number)
        
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            verification = client.verify \
                .v2 \
                .services(self.verify_service_sid) \
                .verifications \
                .create(to=phone_number, channel='sms')
            
            logger.info(f"Verificação enviada com sucesso: {verification.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar verificação: {e}")
            return self._send_email_fallback(phone_number)
    
    def check_verification(self, phone_number, code):
        """Verifica código de verificação via Twilio Verify"""
        if not all([self.account_sid, self.auth_token, self.verify_service_sid]):
            logger.warning("Credenciais Twilio Verify não configuradas.")
            return False
        
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            verification_check = client.verify \
                .v2 \
                .services(self.verify_service_sid) \
                .verification_checks \
                .create(to=phone_number, code=code)
            
            is_valid = verification_check.status == 'approved'
            logger.info(f"Verificação {'aprovada' if is_valid else 'rejeitada'}: {verification_check.sid}")
            return is_valid
            
        except Exception as e:
            logger.error(f"Erro ao verificar código: {e}")
            return False
    
    def _send_email_fallback(self, phone_number):
        """Fallback para email em desenvolvimento"""
        try:
            subject = "Código de Verificação ForgeLock"
            email_message = f"""
            Código de verificação: 123456 (simulado)
            
            Este é um código de verificação para sua conta ForgeLock.
            Se você não solicitou este código, ignore este email.
            """
            
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [f"{phone_number}@example.com"],
                fail_silently=False,
            )
            logger.info(f"Email de fallback enviado para {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"Erro no fallback de email: {e}")
            return False


class VerificationService:
    """Serviço para verificação SMS com Twilio Verify"""
    
    def __init__(self):
        self.twilio_verify = TwilioVerifyService()
        self.expiry_minutes = settings.SMS_VERIFICATION_EXPIRY_MINUTES
    
    def generate_verification_code(self):
        """Gera código de verificação de 6 dígitos (para fallback)"""
        return ''.join(random.choices(string.digits, k=settings.SMS_VERIFICATION_CODE_LENGTH))
    
    def send_verification_code(self, user):
        """Envia código de verificação via Twilio Verify"""
        # Formatar número de telefone
        formatted_number = self._format_phone_number(user.phone_number, user.country.ddi)
        
        # Enviar via Twilio Verify
        success = self.twilio_verify.send_verification(formatted_number)
        
        if success:
            # Salvar informações para tracking
            user.verification_code = 'VERIFY'  # Indica que usa Twilio Verify
            user.verification_expires_at = timezone.now() + timedelta(minutes=self.expiry_minutes)
            user.save()
            logger.info(f"Código de verificação enviado para {formatted_number}")
        else:
            logger.error(f"Falha ao enviar código para {formatted_number}")
        
        return success
    
    def _format_phone_number(self, phone_number, ddi):
        """Formata número de telefone para formato internacional"""
        # Remove caracteres especiais
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Adiciona DDI se não estiver presente
        if not clean_number.startswith(ddi):
            clean_number = ddi + clean_number
        
        # Adiciona + no início
        return f"+{clean_number}"
    
    def verify_code(self, user, code):
        """Verifica código de verificação via Twilio Verify"""
        # Formatar número de telefone
        formatted_number = self._format_phone_number(user.phone_number, user.country.ddi)
        
        # Verificar via Twilio Verify
        is_valid = self.twilio_verify.check_verification(formatted_number, code)
        
        if is_valid:
            user.is_verified = True
            user.verification_code = ''  # String vazia em vez de None
            user.verification_expires_at = None
            user.save()
            return True
        
        return False
    
    def is_code_expired(self, user):
        """Verifica se o código expirou"""
        if not user.verification_expires_at:
            return True
        return timezone.now() > user.verification_expires_at


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


class GeolocationService:
    """Serviço para detectar localização do usuário por IP"""
    
    @staticmethod
    def get_client_ip(request):
        """Obtém o IP real do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def get_country_by_ip(ip):
        """Detecta país por IP usando API gratuita"""
        # Para desenvolvimento local, simular Brasil
        if ip in ['127.0.0.1', 'localhost', '::1']:
            return 'BR'
        
        try:
            # Usar API gratuita do ipapi.co
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data.get('countryCode', 'US')
        except Exception as e:
            logger.warning(f"Erro ao detectar país por IP {ip}: {e}")
        
        return 'US'  # Fallback para EUA
    
    @staticmethod
    def get_currency_by_country(country_code):
        """Mapeia código do país para moeda"""
        currency_mapping = {
            'BR': 'BRL',  # Brasil
            'US': 'USD',  # Estados Unidos
            'CA': 'USD',  # Canadá (usando USD por simplicidade)
            'GB': 'USD',  # Reino Unido (usando USD por simplicidade)
            'DE': 'EUR',  # Alemanha
            'FR': 'EUR',  # França
            'IT': 'EUR',  # Itália
            'ES': 'EUR',  # Espanha
            'NL': 'EUR',  # Holanda
            'BE': 'EUR',  # Bélgica
            'AT': 'EUR',  # Áustria
            'PT': 'EUR',  # Portugal
            'IE': 'EUR',  # Irlanda
            'FI': 'EUR',  # Finlândia
            'SE': 'EUR',  # Suécia
            'DK': 'EUR',  # Dinamarca
            'NO': 'EUR',  # Noruega
            'CH': 'EUR',  # Suíça
        }
        
        return currency_mapping.get(country_code, 'USD')
    
    @staticmethod
    def detect_user_currency(request):
        """Detecta moeda do usuário baseada na localização real (IP)"""
        # Sempre detectar por IP, independente se usuário está logado ou não
        ip = GeolocationService.get_client_ip(request)
        country_code = GeolocationService.get_country_by_ip(ip)
        return GeolocationService.get_currency_by_country(country_code)