from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países no banco de dados'

    def handle(self, *args, **options):
        countries_data = [
            {
                'name': 'Brasil', 
                'name_en': 'Brazil', 
                'name_es': 'Brasil', 
                'code': 'BR', 
                'ddi': '+55', 
                'flag': 'br'
            },
            {
                'name': 'Estados Unidos', 
                'name_en': 'United States', 
                'name_es': 'Estados Unidos', 
                'code': 'US', 
                'ddi': '+1', 
                'flag': 'us'
            },
            {
                'name': 'Argentina', 
                'name_en': 'Argentina', 
                'name_es': 'Argentina', 
                'code': 'AR', 
                'ddi': '+54', 
                'flag': 'ar'
            },
            {
                'name': 'Chile', 
                'name_en': 'Chile', 
                'name_es': 'Chile', 
                'code': 'CL', 
                'ddi': '+56', 
                'flag': 'cl'
            },
            {
                'name': 'Colômbia', 
                'name_en': 'Colombia', 
                'name_es': 'Colombia', 
                'code': 'CO', 
                'ddi': '+57', 
                'flag': 'co'
            },
            {
                'name': 'México', 
                'name_en': 'Mexico', 
                'name_es': 'México', 
                'code': 'MX', 
                'ddi': '+52', 
                'flag': 'mx'
            },
            {
                'name': 'Peru', 
                'name_en': 'Peru', 
                'name_es': 'Perú', 
                'code': 'PE', 
                'ddi': '+51', 
                'flag': 'pe'
            },
            {
                'name': 'Uruguai', 
                'name_en': 'Uruguay', 
                'name_es': 'Uruguay', 
                'code': 'UY', 
                'ddi': '+598', 
                'flag': 'uy'
            },
            {
                'name': 'Venezuela', 
                'name_en': 'Venezuela', 
                'name_es': 'Venezuela', 
                'code': 'VE', 
                'ddi': '+58', 
                'flag': 've'
            },
            {
                'name': 'Espanha', 
                'name_en': 'Spain', 
                'name_es': 'España', 
                'code': 'ES', 
                'ddi': '+34', 
                'flag': 'es'
            },
            {
                'name': 'Portugal', 
                'name_en': 'Portugal', 
                'name_es': 'Portugal', 
                'code': 'PT', 
                'ddi': '+351', 
                'flag': 'pt'
            },
            {
                'name': 'Reino Unido', 
                'name_en': 'United Kingdom', 
                'name_es': 'Reino Unido', 
                'code': 'GB', 
                'ddi': '+44', 
                'flag': 'gb'
            },
            {
                'name': 'França', 
                'name_en': 'France', 
                'name_es': 'Francia', 
                'code': 'FR', 
                'ddi': '+33', 
                'flag': 'fr'
            },
            {
                'name': 'Alemanha', 
                'name_en': 'Germany', 
                'name_es': 'Alemania', 
                'code': 'DE', 
                'ddi': '+49', 
                'flag': 'de'
            },
            {
                'name': 'Itália', 
                'name_en': 'Italy', 
                'name_es': 'Italia', 
                'code': 'IT', 
                'ddi': '+39', 
                'flag': 'it'
            },
        ]

        created_count = 0
        updated_count = 0
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults=country_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'País criado: {country.name}')
            else:
                # Atualizar países existentes com os nomes traduzidos
                country.name_en = country_data['name_en']
                country.name_es = country_data['name_es']
                country.save()
                updated_count += 1
                self.stdout.write(f'País atualizado: {country.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Total de países criados: {created_count}, atualizados: {updated_count}')
        )