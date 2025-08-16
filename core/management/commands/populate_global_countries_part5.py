from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 5/10)'

    def handle(self, *args, **options):
        # PARTE 5: Mais países da Ásia
        countries_data = [
            # Ásia (continuação)
            {'name': 'Bahrein', 'name_en': 'Bahrain', 'name_es': 'Bahrein', 'code': 'BH', 'ddi': '+973', 'flag': 'bh', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Bangladesh', 'name_en': 'Bangladesh', 'name_es': 'Bangladesh', 'code': 'BD', 'ddi': '+880', 'flag': 'bd', 'continent': 'Ásia', 'region': 'Ásia Meridional'},
            {'name': 'Butão', 'name_en': 'Bhutan', 'name_es': 'Bután', 'code': 'BT', 'ddi': '+975', 'flag': 'bt', 'continent': 'Ásia', 'region': 'Ásia Meridional'},
            {'name': 'Brunei', 'name_en': 'Brunei', 'name_es': 'Brunei', 'code': 'BN', 'ddi': '+673', 'flag': 'bn', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Camboja', 'name_en': 'Cambodia', 'name_es': 'Camboya', 'code': 'KH', 'ddi': '+855', 'flag': 'kh', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Cazaquistão', 'name_en': 'Kazakhstan', 'name_es': 'Kazajistán', 'code': 'KZ', 'ddi': '+7', 'flag': 'kz', 'continent': 'Ásia', 'region': 'Ásia Central'},
            {'name': 'China', 'name_en': 'China', 'name_es': 'China', 'code': 'CN', 'ddi': '+86', 'flag': 'cn', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Coreia do Norte', 'name_en': 'North Korea', 'name_es': 'Corea del Norte', 'code': 'KP', 'ddi': '+850', 'flag': 'kp', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Coreia do Sul', 'name_en': 'South Korea', 'name_es': 'Corea del Sur', 'code': 'KR', 'ddi': '+82', 'flag': 'kr', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Emirados Árabes Unidos', 'name_en': 'United Arab Emirates', 'name_es': 'Emiratos Árabes Unidos', 'code': 'AE', 'ddi': '+971', 'flag': 'ae', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Filipinas', 'name_en': 'Philippines', 'name_es': 'Filipinas', 'code': 'PH', 'ddi': '+63', 'flag': 'ph', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Geórgia', 'name_en': 'Georgia', 'name_es': 'Georgia', 'code': 'GE', 'ddi': '+995', 'flag': 'ge', 'continent': 'Ásia', 'region': 'Cáucaso'},
            {'name': 'Índia', 'name_en': 'India', 'name_es': 'India', 'code': 'IN', 'ddi': '+91', 'flag': 'in', 'continent': 'Ásia', 'region': 'Ásia Meridional'},
            {'name': 'Indonésia', 'name_en': 'Indonesia', 'name_es': 'Indonesia', 'code': 'ID', 'ddi': '+62', 'flag': 'id', 'continent': 'Ásia', 'region': 'Sudeste Asiático'},
            {'name': 'Irã', 'name_en': 'Iran', 'name_es': 'Irán', 'code': 'IR', 'ddi': '+98', 'flag': 'ir', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Iraque', 'name_en': 'Iraq', 'name_es': 'Irak', 'code': 'IQ', 'ddi': '+964', 'flag': 'iq', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Israel', 'name_en': 'Israel', 'name_es': 'Israel', 'code': 'IL', 'ddi': '+972', 'flag': 'il', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Japão', 'name_en': 'Japan', 'name_es': 'Japón', 'code': 'JP', 'ddi': '+81', 'flag': 'jp', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Jordânia', 'name_en': 'Jordan', 'name_es': 'Jordania', 'code': 'JO', 'ddi': '+962', 'flag': 'jo', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Kuwait', 'name_en': 'Kuwait', 'name_es': 'Kuwait', 'code': 'KW', 'ddi': '+965', 'flag': 'kw', 'continent': 'Ásia', 'region': 'Oriente Médio'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 5/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 5 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part6')
