from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Country, Plan, Account

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria o usuário rasilva84'

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
        
        # Criar usuário rasilva84
        rasilva_user, created = User.objects.get_or_create(
            username='rasilva84',
            defaults={
                'email': 'rasilva84@gmail.com',
                'phone_number': '+5511999999999',
                'country': brazil,
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            # Definir senha (você pode alterar depois)
            rasilva_user.set_password('rasilva123')
            rasilva_user.save()
            
            # Criar account para rasilva84
            Account.objects.create(user=rasilva_user, plan=admin_plan)
            
            self.stdout.write(self.style.SUCCESS('Usuário rasilva84 criado com sucesso!'))
            self.stdout.write('Username: rasilva84')
            self.stdout.write('Password: rasilva123')
            self.stdout.write('Email: rasilva84@gmail.com')
        else:
            self.stdout.write(self.style.WARNING('Usuário rasilva84 já existe'))
            
        # Listar todos os usuários admin
        self.stdout.write(self.style.SUCCESS('\n=== USUÁRIOS ADMIN ==='))
        admin_users = User.objects.filter(is_superuser=True)
        for user in admin_users:
            self.stdout.write(f'- {user.username} ({user.email}) - {"✅ Verificado" if user.is_verified else "❌ Não verificado"}')
            
        self.stdout.write(self.style.SUCCESS('\n=== CREDENCIAIS DE ACESSO ==='))
        self.stdout.write('Admin: rasilva84 / rasilva123')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('\nURLs:')
        self.stdout.write('- Admin: http://localhost:8000/admin/')
        self.stdout.write('- Sistema: http://localhost:8000/')