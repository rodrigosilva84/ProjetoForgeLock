from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Country, Plan, Account

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria usuário admin para o sistema'

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
        
        # Criar usuário admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@forgelock.com',
                'phone_number': '+5511999999999',
                'country': brazil,
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            
            # Criar account para admin
            Account.objects.create(user=admin_user, plan=admin_plan)
            
            self.stdout.write(self.style.SUCCESS('Usuário admin criado com sucesso!'))
            self.stdout.write('Username: admin')
            self.stdout.write('Password: admin123')
            self.stdout.write('Email: admin@forgelock.com')
        else:
            self.stdout.write(self.style.WARNING('Usuário admin já existe'))
            
        self.stdout.write(self.style.SUCCESS('\n=== CREDENCIAIS DE ACESSO ==='))
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('\nURLs:')
        self.stdout.write('- Admin: http://localhost:8000/admin/')
        self.stdout.write('- Sistema: http://localhost:8000/')