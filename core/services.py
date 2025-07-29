import os
import random
import string
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import logging

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
    """Serviço para gerenciamento de códigos de verificação"""
    
    def __init__(self):
        self.sms_service = SMSService()
        self.code_length = settings.SMS_VERIFICATION_CODE_LENGTH
        self.expiry_minutes = settings.SMS_VERIFICATION_EXPIRY_MINUTES
    
    def generate_code(self):
        """Gera código de verificação"""
        return ''.join(random.choices(string.digits, k=self.code_length))
    
    def send_verification_code(self, user):
        """Envia código de verificação para o usuário"""
        code = self.generate_code()
        expiry = timezone.now() + timedelta(minutes=self.expiry_minutes)
        
        # Salvar código no usuário
        user.verification_code = code
        user.verification_expires = expiry
        user.save()
        
        # Mensagem SMS
        message = f"Seu código de verificação ForgeLock é: {code}. Válido por {self.expiry_minutes} minutos."
        
        # Enviar SMS
        success = self.sms_service.send_sms(user.phone_number, message)
        
        if success:
            logger.info(f"Código de verificação enviado para {user.phone_number}")
            return True
        else:
            logger.error(f"Falha ao enviar código para {user.phone_number}")
            return False
    
    def verify_code(self, user, code):
        """Verifica se o código está correto e não expirou"""
        if not user.verification_code or not user.verification_expires:
            return False
        
        if user.verification_code != code:
            return False
        
        if timezone.now() > user.verification_expires:
            return False
        
        # Código válido - marcar usuário como verificado
        user.is_verified = True
        user.verification_code = ''
        user.verification_expires = None
        user.save()
        
        logger.info(f"Usuário {user.username} verificado com sucesso")
        return True
    
    def is_code_expired(self, user):
        """Verifica se o código expirou"""
        if not user.verification_expires:
            return True
        return timezone.now() > user.verification_expires