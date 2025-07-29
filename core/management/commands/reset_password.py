from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Redefine a senha do usuário especificado'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nome de usuário')
        parser.add_argument('new_password', type=str, help='Nova senha')

    def handle(self, *args, **options):
        username = options['username']
        new_password = options['new_password']
        
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Senha redefinida com sucesso para o usuário: {username}')
            )
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Nova senha: {new_password}')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuário "{username}" não encontrado.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao redefinir senha: {e}')
            )