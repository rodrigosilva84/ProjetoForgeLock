from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 1/10)'

    def handle(self, *args, **options):
        # PARTE 1: Primeiros 20 países (África e América do Norte)
        countries_data = [
            # África
            {'name': 'África do Sul', 'name_en': 'South Africa', 'name_es': 'Sudáfrica', 'code': 'ZA', 'ddi': '+27', 'flag': 'za', 'continent': 'África', 'region': 'África Austral'},
            {'name': 'Angola', 'name_en': 'Angola', 'name_es': 'Angola', 'code': 'AO', 'ddi': '+244', 'flag': 'ao', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Argélia', 'name_en': 'Algeria', 'name_es': 'Argelia', 'code': 'DZ', 'ddi': '+213', 'flag': 'dz', 'continent': 'África', 'region': 'África do Norte'},
            {'name': 'Benim', 'name_en': 'Benin', 'name_es': 'Benín', 'code': 'BJ', 'ddi': '+229', 'flag': 'bj', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Botsuana', 'name_en': 'Botswana', 'name_es': 'Botsuana', 'code': 'BW', 'ddi': '+267', 'flag': 'bw', 'continent': 'África', 'region': 'África Austral'},
            {'name': 'Burkina Faso', 'name_en': 'Burkina Faso', 'name_es': 'Burkina Faso', 'code': 'BF', 'ddi': '+226', 'flag': 'bf', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Burundi', 'name_en': 'Burundi', 'name_es': 'Burundi', 'code': 'BI', 'ddi': '+257', 'flag': 'bi', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Camarões', 'name_en': 'Cameroon', 'name_es': 'Camerún', 'code': 'CM', 'ddi': '+237', 'flag': 'cm', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Chade', 'name_en': 'Chad', 'name_es': 'Chad', 'code': 'TD', 'ddi': '+235', 'flag': 'td', 'continent': 'África', 'region': 'África Central'},
            {'name': 'Comores', 'name_en': 'Comoros', 'name_es': 'Comoras', 'code': 'KM', 'ddi': '+269', 'flag': 'km', 'continent': 'África', 'region': 'África Oriental'},
            
            # América do Norte
            {'name': 'Canadá', 'name_en': 'Canada', 'name_es': 'Canadá', 'code': 'CA', 'ddi': '+1', 'flag': 'ca', 'continent': 'América do Norte', 'region': 'América Anglo-Saxônica'},
            {'name': 'Estados Unidos', 'name_en': 'United States', 'name_es': 'Estados Unidos', 'code': 'US', 'ddi': '+1', 'flag': 'us', 'continent': 'América do Norte', 'region': 'América Anglo-Saxônica'},
            {'name': 'México', 'name_en': 'Mexico', 'name_es': 'México', 'code': 'MX', 'ddi': '+52', 'flag': 'mx', 'continent': 'América do Norte', 'region': 'América Latina'},
            
            # América Central
            {'name': 'Belize', 'name_en': 'Belize', 'name_es': 'Belice', 'code': 'BZ', 'ddi': '+501', 'flag': 'bz', 'continent': 'América Central', 'region': 'América Latina'},
            {'name': 'Costa Rica', 'name_en': 'Costa Rica', 'name_es': 'Costa Rica', 'code': 'CR', 'ddi': '+506', 'flag': 'cr', 'continent': 'América Central', 'region': 'América Latina'},
            {'name': 'El Salvador', 'name_en': 'El Salvador', 'name_es': 'El Salvador', 'code': 'SV', 'ddi': '+503', 'flag': 'sv', 'continent': 'América Central', 'region': 'América Latina'},
            {'name': 'Guatemala', 'name_en': 'Guatemala', 'name_es': 'Guatemala', 'code': 'GT', 'ddi': '+502', 'flag': 'gt', 'continent': 'América Central', 'region': 'América Latina'},
            {'name': 'Honduras', 'name_en': 'Honduras', 'name_es': 'Honduras', 'code': 'HN', 'ddi': '+504', 'flag': 'hn', 'continent': 'América Central', 'region': 'América Latina'},
            {'name': 'Nicarágua', 'name_en': 'Nicaragua', 'name_es': 'Nicaragua', 'code': 'NI', 'ddi': '+505', 'flag': 'ni', 'continent': 'América Central', 'region': 'América Latina'},
            {'name': 'Panamá', 'name_en': 'Panama', 'name_es': 'Panamá', 'code': 'PA', 'ddi': '+507', 'flag': 'pa', 'continent': 'América Central', 'region': 'América Latina'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 1/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 1 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part2')
