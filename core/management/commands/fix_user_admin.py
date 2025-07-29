from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Country, Plan, Account

User = get_user_model()

class Command(BaseCommand):
    help = 'Corrige o usuário admin existente'

    def handle(self, *args, **options):
        # Obter Brasil como país padrão
        brazil = Country.objects.get(code='BR')
        
        # Criar plano admin se não existir
        admin_plan, created = Plan.objects.get_or_create(
            name="Admin",
            defaults={
                'description': "Plano administrativo",
                'price': 0,
                'max_users': 999,
                'max_customers': 999999,
                'max_products': 999999,
                'max_projects': 999999,
                'has_stl_security': True,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Plano admin criado: {admin_plan.name}'))
        
        # Verificar se existe o usuário rasilva84
        try:
            user = User.objects.get(username='rasilva84')
            self.stdout.write(self.style.SUCCESS(f'Usuário encontrado: {user.username}'))
            
            # Atualizar campos obrigatórios se necessário
            if not user.country:
                user.country = brazil
                self.stdout.write('País atualizado para Brasil')
            
            if not user.is_verified:
                user.is_verified = True
                self.stdout.write('Usuário marcado como verificado')
            
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            # Criar account se não existir
            account, created = Account.objects.get_or_create(
                user=user,
                defaults={'plan': admin_plan}
            )
            
            if created:
                self.stdout.write('Account criada para o usuário')
            
            self.stdout.write(self.style.SUCCESS('Usuário rasilva84 atualizado com sucesso!'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('Usuário rasilva84 não encontrado'))
            
        # Listar todos os usuários admin
        self.stdout.write(self.style.SUCCESS('\n=== USUÁRIOS ADMIN ==='))
        admin_users = User.objects.filter(is_superuser=True)
        for user in admin_users:
            self.stdout.write(f'- {user.username} ({user.email}) - {"✅ Verificado" if user.is_verified else "❌ Não verificado"}')
            
        self.stdout.write(self.style.SUCCESS('\n=== CREDENCIAIS DE ACESSO ==='))
        self.stdout.write('Admin: rasilva84 / (sua senha)')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('\nURLs:')
        self.stdout.write('- Admin: http://localhost:8000/admin/')
        self.stdout.write('- Sistema: http://localhost:8000/')