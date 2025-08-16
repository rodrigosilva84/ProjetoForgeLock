from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 7/10)'

    def handle(self, *args, **options):
        # PARTE 7: Final da Ásia e início da Oceania
        countries_data = [
            # Ásia (final)
            {'name': 'Vietnã', 'name_en': 'Vietnam', 'name_es': 'Vietnam', 'code': 'VN', 'ddi': '+84', 'flag': 'vn', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Iêmen', 'name_en': 'Yemen', 'name_es': 'Yemen', 'code': 'YE', 'ddi': '+967', 'flag': 'ye', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            
            # Oceania
            {'name': 'Austrália', 'name_en': 'Australia', 'name_es': 'Australia', 'code': 'AU', 'ddi': '+61', 'flag': 'au', 'continent': 'Oceania', 'region': 'Australásia'},
            {'name': 'Fiji', 'name_en': 'Fiji', 'name_es': 'Fiyi', 'code': 'FJ', 'ddi': '+679', 'flag': 'fj', 'continent': 'Oceania', 'region': 'Melanésia'},
            {'name': 'Kiribati', 'name_en': 'Kiribati', 'name_es': 'Kiribati', 'code': 'KI', 'ddi': '+686', 'flag': 'ki', 'continent': 'Oceania', 'region': 'Micronésia'},
            {'name': 'Micronésia', 'name_en': 'Micronesia', 'name_es': 'Micronesia', 'code': 'FM', 'ddi': '+691', 'flag': 'fm', 'continent': 'Oceania', 'region': 'Micronésia'},
            {'name': 'Nauru', 'name_en': 'Nauru', 'name_es': 'Nauru', 'code': 'NR', 'ddi': '+674', 'flag': 'nr', 'continent': 'Oceania', 'region': 'Micronésia'},
            {'name': 'Nova Zelândia', 'name_en': 'New Zealand', 'name_es': 'Nueva Zelanda', 'code': 'NZ', 'ddi': '+64', 'flag': 'nz', 'continent': 'Oceania', 'region': 'Australásia'},
            {'name': 'Palau', 'name_en': 'Palau', 'name_es': 'Palaos', 'code': 'PW', 'ddi': '+680', 'flag': 'pw', 'continent': 'Oceania', 'region': 'Micronésia'},
            {'name': 'Papua-Nova Guiné', 'name_en': 'Papua New Guinea', 'name_es': 'Papua Nueva Guinea', 'code': 'PG', 'ddi': '+675', 'flag': 'pg', 'continent': 'Oceania', 'region': 'Melanésia'},
            {'name': 'Samoa', 'name_en': 'Samoa', 'name_es': 'Samoa', 'code': 'WS', 'ddi': '+685', 'flag': 'ws', 'continent': 'Oceania', 'region': 'Polinésia'},
            {'name': 'Ilhas Salomão', 'name_en': 'Solomon Islands', 'name_es': 'Islas Salomón', 'code': 'SB', 'ddi': '+677', 'flag': 'sb', 'continent': 'Oceania', 'region': 'Melanésia'},
            {'name': 'Tonga', 'name_en': 'Tonga', 'name_es': 'Tonga', 'code': 'TO', 'ddi': '+676', 'flag': 'to', 'continent': 'Oceania', 'region': 'Polinésia'},
            {'name': 'Tuvalu', 'name_en': 'Tuvalu', 'name_es': 'Tuvalu', 'code': 'TV', 'ddi': '+688', 'flag': 'tv', 'continent': 'Oceania', 'region': 'Polinésia'},
            {'name': 'Vanuatu', 'name_en': 'Vanuatu', 'name_es': 'Vanuatu', 'code': 'VU', 'ddi': '+678', 'flag': 'vu', 'continent': 'Oceania', 'region': 'Melanésia'},
            
            # Caribe (continuação)
            {'name': 'Antígua e Barbuda', 'name_en': 'Antigua and Barbuda', 'name_es': 'Antigua y Barbuda', 'code': 'AG', 'ddi': '+1', 'flag': 'ag', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Bahamas', 'name_en': 'Bahamas', 'name_es': 'Bahamas', 'code': 'BS', 'ddi': '+1', 'flag': 'bs', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Barbados', 'name_en': 'Barbados', 'name_es': 'Barbados', 'code': 'BB', 'ddi': '+1', 'flag': 'bb', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Cuba', 'name_en': 'Cuba', 'name_es': 'Cuba', 'code': 'CU', 'ddi': '+53', 'flag': 'cu', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Dominica', 'name_en': 'Dominica', 'name_es': 'Dominica', 'code': 'DM', 'ddi': '+1', 'flag': 'dm', 'continent': 'América do Norte', 'region': 'Caribe'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 7/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 7 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part8')
