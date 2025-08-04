from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageMiddleware(MiddlewareMixin):
    """Middleware para gerenciar o idioma da aplicação"""
    
    def process_request(self, request):
        # Verificar se há um idioma na sessão
        session_language = request.session.get('django_language')
        if session_language:
            translation.activate(session_language)
        else:
            # Usar o idioma padrão
            translation.activate('pt')
        
        # Adicionar o idioma atual ao request
        request.LANGUAGE_CODE = translation.get_language() 