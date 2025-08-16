from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 6/10)'

    def handle(self, *args, **options):
        # PARTE 6: Mais países da Ásia e início da Oceania
        countries_data = [
            # Ásia (continuação)
            {'name': 'Laos', 'name_en': 'Laos', 'name_es': 'Laos', 'code': 'LA', 'ddi': '+856', 'flag': 'la', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Líbano', 'name_en': 'Lebanon', 'name_es': 'Líbano', 'code': 'LB', 'ddi': '+961', 'flag': 'lb', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Malásia', 'name_en': 'Malaysia', 'name_es': 'Malasia', 'code': 'MY', 'ddi': '+60', 'flag': 'my', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Maldivas', 'name_en': 'Maldives', 'name_es': 'Maldivas', 'code': 'MV', 'ddi': '+960', 'flag': 'mv', 'continent': 'Ásia', 'region': 'Ásia Meridional'},
            {'name': 'Mianmar', 'name_en': 'Myanmar', 'name_es': 'Myanmar', 'code': 'MM', 'ddi': '+95', 'flag': 'mm', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Mongólia', 'name_en': 'Mongolia', 'name_es': 'Mongolia', 'code': 'MN', 'ddi': '+976', 'flag': 'mn', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Nepal', 'name_en': 'Nepal', 'name_es': 'Nepal', 'code': 'NP', 'ddi': '+977', 'flag': 'np', 'continent': 'Ásia', 'region': 'Ásia Meridional'},
            {'name': 'Omã', 'name_en': 'Oman', 'name_es': 'Omán', 'code': 'OM', 'ddi': '+968', 'flag': 'om', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Paquistão', 'name_en': 'Pakistan', 'name_es': 'Pakistán', 'code': 'PK', 'ddi': '+92', 'flag': 'pk', 'continent': 'Ásia', 'region': 'Ásia Meridional'},
            {'name': 'Qatar', 'name_en': 'Qatar', 'name_es': 'Qatar', 'code': 'QA', 'ddi': '+974', 'flag': 'qa', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Quirguistão', 'name_en': 'Kyrgyzstan', 'name_es': 'Kirguistán', 'code': 'KG', 'ddi': '+996', 'flag': 'kg', 'continent': 'Ásia', 'region': 'Ásia Central'},
            {'name': 'Singapura', 'name_en': 'Singapore', 'name_es': 'Singapur', 'code': 'SG', 'ddi': '+65', 'flag': 'sg', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Síria', 'name_en': 'Syria', 'name_es': 'Siria', 'code': 'SY', 'ddi': '+963', 'flag': 'sy', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Sri Lanka', 'name_en': 'Sri Lanka', 'name_es': 'Sri Lanka', 'code': 'LK', 'ddi': '+94', 'flag': 'lk', 'continent': 'Ásia', 'region': 'Ásia Meridional'},
            {'name': 'Tajiquistão', 'name_en': 'Tajikistan', 'name_es': 'Tayikistán', 'code': 'TJ', 'ddi': '+992', 'flag': 'tj', 'continent': 'Ásia', 'region': 'Ásia Central'},
            {'name': 'Tailândia', 'name_en': 'Thailand', 'name_es': 'Tailandia', 'code': 'TH', 'ddi': '+66', 'flag': 'th', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Taiwan', 'name_en': 'Taiwan', 'name_es': 'Taiwán', 'code': 'TW', 'ddi': '+886', 'flag': 'tw', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Timor-Leste', 'name_en': 'Timor-Leste', 'name_es': 'Timor Oriental', 'code': 'TL', 'ddi': '+670', 'flag': 'tl', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Turcomenistão', 'name_en': 'Turkmenistan', 'name_es': 'Turkmenistán', 'code': 'TM', 'ddi': '+993', 'flag': 'tm', 'continent': 'Ásia', 'region': 'Ásia Central'},
            {'name': 'Uzbequistão', 'name_en': 'Uzbekistan', 'name_es': 'Uzbekistán', 'code': 'UZ', 'ddi': '+998', 'flag': 'uz', 'continent': 'Ásia', 'region': 'Ásia Central'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 6/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 6 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part7')
