from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 8/10)'

    def handle(self, *args, **options):
        # PARTE 8: Final do Caribe e mais países da África
        countries_data = [
            # Caribe (final)
            {'name': 'Granada', 'name_en': 'Grenada', 'name_es': 'Granada', 'code': 'GD', 'ddi': '+1', 'flag': 'gd', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Haiti', 'name_en': 'Haiti', 'name_es': 'Haití', 'code': 'HT', 'ddi': '+509', 'flag': 'ht', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Jamaica', 'name_en': 'Jamaica', 'name_es': 'Jamaica', 'code': 'JM', 'ddi': '+1', 'flag': 'jm', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'República Dominicana', 'name_en': 'Dominican Republic', 'name_es': 'República Dominicana', 'code': 'DO', 'ddi': '+1', 'flag': 'do', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Santa Lúcia', 'name_en': 'Saint Lucia', 'name_es': 'Santa Lucía', 'code': 'LC', 'ddi': '+1', 'flag': 'lc', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'São Cristóvão e Névis', 'name_en': 'Saint Kitts and Nevis', 'name_es': 'San Cristóbal y Nieves', 'code': 'KN', 'ddi': '+1', 'flag': 'kn', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'São Vicente e Granadinas', 'name_en': 'Saint Vincent and the Grenadines', 'name_es': 'San Vicente y las Granadinas', 'code': 'VC', 'ddi': '+1', 'flag': 'vc', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Trinidad e Tobago', 'name_en': 'Trinidad and Tobago', 'name_es': 'Trinidad y Tobago', 'code': 'TT', 'ddi': '+1', 'flag': 'tt', 'continent': 'América do Norte', 'region': 'Caribe'},
            
            # África (continuação)
            {'name': 'Congo', 'name_en': 'Congo', 'name_es': 'Congo', 'code': 'CG', 'ddi': '+242', 'flag': 'cg', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Costa do Marfim', 'name_en': 'Ivory Coast', 'name_es': 'Costa de Marfil', 'code': 'CI', 'ddi': '+225', 'flag': 'ci', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Djibouti', 'name_en': 'Djibouti', 'name_es': 'Yibuti', 'code': 'DJ', 'ddi': '+253', 'flag': 'dj', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Egito', 'name_en': 'Egypt', 'name_es': 'Egipto', 'code': 'EG', 'ddi': '+20', 'flag': 'eg', 'continent': 'África', 'region': 'África do Norte'},
            {'name': 'Eritreia', 'name_en': 'Eritrea', 'name_es': 'Eritrea', 'code': 'ER', 'ddi': '+291', 'flag': 'er', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Etiópia', 'name_en': 'Ethiopia', 'name_es': 'Etiopía', 'code': 'ET', 'ddi': '+251', 'flag': 'et', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Gabão', 'name_en': 'Gabon', 'name_es': 'Gabón', 'code': 'GA', 'ddi': '+241', 'flag': 'ga', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Gâmbia', 'name_en': 'Gambia', 'name_es': 'Gambia', 'code': 'GM', 'ddi': '+220', 'flag': 'gm', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Gana', 'name_en': 'Ghana', 'name_es': 'Ghana', 'code': 'GH', 'ddi': '+233', 'flag': 'gh', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Guiné', 'name_en': 'Guinea', 'name_es': 'Guinea', 'code': 'GN', 'ddi': '+224', 'flag': 'gn', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Guiné-Bissau', 'name_en': 'Guinea-Bissau', 'name_es': 'Guinea-Bisáu', 'code': 'GW', 'ddi': '+245', 'flag': 'gw', 'continent': 'África', 'region': 'África Ocidental'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 8/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 8 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part9')
