from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países no banco de dados'

    def handle(self, *args, **options):
        countries_data = [
            {'name': 'Brasil', 'code': 'BR', 'ddi': '+55', 'flag': 'br'},
            {'name': 'Estados Unidos', 'code': 'US', 'ddi': '+1', 'flag': 'us'},
            {'name': 'Argentina', 'code': 'AR', 'ddi': '+54', 'flag': 'ar'},
            {'name': 'Chile', 'code': 'CL', 'ddi': '+56', 'flag': 'cl'},
            {'name': 'Colômbia', 'code': 'CO', 'ddi': '+57', 'flag': 'co'},
            {'name': 'México', 'code': 'MX', 'ddi': '+52', 'flag': 'mx'},
            {'name': 'Peru', 'code': 'PE', 'ddi': '+51', 'flag': 'pe'},
            {'name': 'Uruguai', 'code': 'UY', 'ddi': '+598', 'flag': 'uy'},
            {'name': 'Venezuela', 'code': 'VE', 'ddi': '+58', 'flag': 've'},
            {'name': 'Espanha', 'code': 'ES', 'ddi': '+34', 'flag': 'es'},
            {'name': 'Portugal', 'code': 'PT', 'ddi': '+351', 'flag': 'pt'},
            {'name': 'Reino Unido', 'code': 'GB', 'ddi': '+44', 'flag': 'gb'},
            {'name': 'França', 'code': 'FR', 'ddi': '+33', 'flag': 'fr'},
            {'name': 'Alemanha', 'code': 'DE', 'ddi': '+49', 'flag': 'de'},
            {'name': 'Itália', 'code': 'IT', 'ddi': '+39', 'flag': 'it'},
        ]

        created_count = 0
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults=country_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'País criado: {country.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Total de países criados: {created_count}')
        )