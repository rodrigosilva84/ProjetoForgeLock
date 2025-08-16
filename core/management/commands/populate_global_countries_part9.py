from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 9/10)'

    def handle(self, *args, **options):
        # PARTE 9: Final da África
        countries_data = [
            # África (final)
            {'name': 'Guiné Equatorial', 'name_en': 'Equatorial Guinea', 'name_es': 'Guinea Ecuatorial', 'code': 'GQ', 'ddi': '+240', 'flag': 'gq', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Quênia', 'name_en': 'Kenya', 'name_es': 'Kenia', 'code': 'KE', 'ddi': '+254', 'flag': 'ke', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Lesoto', 'name_en': 'Lesotho', 'name_es': 'Lesoto', 'code': 'LS', 'ddi': '+266', 'flag': 'ls', 'continent': 'África', 'region': 'África Austral'},
            {'name': 'Libéria', 'name_en': 'Liberia', 'name_es': 'Liberia', 'code': 'LR', 'ddi': '+231', 'flag': 'lr', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Líbia', 'name_en': 'Libya', 'name_es': 'Libia', 'code': 'LY', 'ddi': '+218', 'flag': 'ly', 'continent': 'África', 'region': 'África do Norte'},
            {'name': 'Madagascar', 'name_en': 'Madagascar', 'name_es': 'Madagascar', 'code': 'MG', 'ddi': '+261', 'flag': 'mg', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Malawi', 'name_en': 'Malawi', 'name_es': 'Malawi', 'code': 'MW', 'ddi': '+265', 'flag': 'mw', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Mali', 'name_en': 'Mali', 'name_es': 'Malí', 'code': 'ML', 'ddi': '+223', 'flag': 'ml', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Mauritânia', 'name_en': 'Mauritania', 'name_es': 'Mauritania', 'code': 'MR', 'ddi': '+222', 'flag': 'mr', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Maurício', 'name_en': 'Mauritius', 'name_es': 'Mauricio', 'code': 'MU', 'ddi': '+230', 'flag': 'mu', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Marrocos', 'name_en': 'Morocco', 'name_es': 'Marruecos', 'code': 'MA', 'ddi': '+212', 'flag': 'ma', 'continent': 'África', 'region': 'África do Norte'},
            {'name': 'Moçambique', 'name_en': 'Mozambique', 'name_es': 'Mozambique', 'code': 'MZ', 'ddi': '+258', 'flag': 'mz', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Namíbia', 'name_en': 'Namibia', 'name_es': 'Namibia', 'code': 'NA', 'ddi': '+264', 'flag': 'na', 'continent': 'África', 'region': 'África Austral'},
            {'name': 'Níger', 'name_en': 'Niger', 'name_es': 'Níger', 'code': 'NE', 'ddi': '+227', 'flag': 'ne', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Nigéria', 'name_en': 'Nigeria', 'name_es': 'Nigeria', 'code': 'NG', 'ddi': '+234', 'flag': 'ng', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'República Centro-Africana', 'name_en': 'Central African Republic', 'name_es': 'República Centroafricana', 'code': 'CF', 'ddi': '+236', 'flag': 'cf', 'continent': 'África', 'region': 'África Central'},
            {'name': 'República Democrática do Congo', 'name_en': 'Democratic Republic of the Congo', 'name_es': 'República Democrática del Congo', 'code': 'CD', 'ddi': '+243', 'flag': 'cd', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Ruanda', 'name_en': 'Rwanda', 'name_es': 'Ruanda', 'code': 'RW', 'ddi': '+250', 'flag': 'rw', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'São Tomé e Príncipe', 'name_en': 'São Tomé and Príncipe', 'name_es': 'Santo Tomé y Príncipe', 'code': 'ST', 'ddi': '+239', 'flag': 'st', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Senegal', 'name_en': 'Senegal', 'name_es': 'Senegal', 'code': 'SN', 'ddi': '+221', 'flag': 'sn', 'continent': 'África', 'region': 'África Ocidental'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 9/10)...')
        
        for country_data in countries_data:
            try:
                country, created = Country.objects.update_or_create(
                    code=country_data['code'],
                    defaults={
                        'name': country_data['name'],
                        'name_en': country_data['name_en'],
                        'name_es': country_data['name_es'],
                        'ddi': country_data['ddi'],
                        'flag': country_data['flag'],
                        'continent': country_data['continent'],
                        'region': country_data['region'],
                        'is_active': True
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'✅ País criado: {country.name} ({country.continent})')
                else:
                    updated_count += 1
                    self.stdout.write(f'🔄 País atualizado: {country.name} ({country.continent})')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao processar {country_data["name"]}: {str(e)}')
                )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Parte 9 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part10')
