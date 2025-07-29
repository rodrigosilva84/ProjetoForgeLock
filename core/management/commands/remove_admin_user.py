from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Remove o usuário admin padrão'

    def handle(self, *args, **options):
        try:
            # Remover usuário admin padrão
            admin_user = User.objects.get(username='admin')
            admin_user.delete()
            self.stdout.write(self.style.SUCCESS('Usuário admin removido com sucesso!'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('Usuário admin não encontrado'))
            
        # Listar usuários admin restantes
        self.stdout.write(self.style.SUCCESS('\n=== USUÁRIOS ADMIN RESTANTES ==='))
        admin_users = User.objects.filter(is_superuser=True)
        if admin_users.exists():
            for user in admin_users:
                self.stdout.write(f'- {user.username} ({user.email}) - {"✅ Verificado" if user.is_verified else "❌ Não verificado"}')
        else:
            self.stdout.write('Nenhum usuário admin encontrado')
            
        self.stdout.write(self.style.SUCCESS('\n=== CREDENCIAIS DE ACESSO ==='))
        self.stdout.write('Admin: rasilva84 / rasilva123')
        self.stdout.write('\nURLs:')
        self.stdout.write('- Admin: http://localhost:8000/admin/')
        self.stdout.write('- Sistema: http://localhost:8000/')