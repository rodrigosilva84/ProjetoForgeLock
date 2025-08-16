from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 4/10)'

    def handle(self, *args, **options):
        # PARTE 4: Final da Europa e início da Ásia
        countries_data = [
            # Europa (final)
            {'name': 'Mônaco', 'name_en': 'Monaco', 'name_es': 'Mónaco', 'code': 'MC', 'ddi': '+377', 'flag': 'mc', 'continent': 'Europa', 'region': 'Europa Meridional'},
            {'name': 'Montenegro', 'name_en': 'Montenegro', 'name_es': 'Montenegro', 'code': 'ME', 'ddi': '+382', 'flag': 'me', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Noruega', 'name_en': 'Norway', 'name_es': 'Noruega', 'code': 'NO', 'ddi': '+47', 'flag': 'no', 'continent': 'Europa', 'region': 'Escandinávia'},
            {'name': 'Países Baixos', 'name_en': 'Netherlands', 'name_es': 'Países Bajos', 'code': 'NL', 'ddi': '+31', 'flag': 'nl', 'continent': 'Europa', 'region': 'Europa Ocidental'},
            {'name': 'Polônia', 'name_en': 'Poland', 'name_es': 'Polonia', 'code': 'PL', 'ddi': '+48', 'flag': 'pl', 'continent': 'Europa', 'region': 'Europa Central'},
            {'name': 'Portugal', 'name_en': 'Portugal', 'name_es': 'Portugal', 'code': 'PT', 'ddi': '+351', 'flag': 'pt', 'continent': 'Europa', 'region': 'Península Ibérica'},
            {'name': 'Reino Unido', 'name_en': 'United Kingdom', 'name_es': 'Reino Unido', 'code': 'GB', 'ddi': '+44', 'flag': 'gb', 'continent': 'Europa', 'region': 'Ilhas Britânicas'},
            {'name': 'República Tcheca', 'name_en': 'Czech Republic', 'name_es': 'República Checa', 'code': 'CZ', 'ddi': '+420', 'flag': 'cz', 'continent': 'Europa', 'region': 'Europa Central'},
            {'name': 'Romênia', 'name_en': 'Romania', 'name_es': 'Rumania', 'code': 'RO', 'ddi': '+40', 'flag': 'ro', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Rússia', 'name_en': 'Russia', 'name_es': 'Rusia', 'code': 'RU', 'ddi': '+7', 'flag': 'ru', 'continent': 'Europa', 'region': 'Europa Oriental'},
            {'name': 'San Marino', 'name_en': 'San Marino', 'name_es': 'San Marino', 'code': 'SM', 'ddi': '+378', 'flag': 'sm', 'continent': 'Europa', 'region': 'Europa Meridional'},
            {'name': 'Sérvia', 'name_en': 'Serbia', 'name_es': 'Serbia', 'code': 'RS', 'ddi': '+381', 'flag': 'rs', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Suécia', 'name_en': 'Sweden', 'name_es': 'Suecia', 'code': 'SE', 'ddi': '+46', 'flag': 'se', 'continent': 'Europa', 'region': 'Escandinávia'},
            {'name': 'Suíça', 'name_en': 'Switzerland', 'name_es': 'Suiza', 'code': 'CH', 'ddi': '+41', 'flag': 'ch', 'continent': 'Europa', 'region': 'Europa Central'},
            {'name': 'Ucrânia', 'name_en': 'Ukraine', 'name_es': 'Ucrania', 'code': 'UA', 'ddi': '+380', 'flag': 'ua', 'continent': 'Europa', 'region': 'Europa Oriental'},
            {'name': 'Vaticano', 'name_en': 'Vatican City', 'name_es': 'Ciudad del Vaticano', 'code': 'VA', 'ddi': '+379', 'flag': 'va', 'continent': 'Europa', 'region': 'Europa Meridional'},
            
            # Ásia (início)
            {'name': 'Afeganistão', 'name_en': 'Afghanistan', 'name_es': 'Afganistán', 'code': 'AF', 'ddi': '+93', 'flag': 'af', 'continent': 'Ásia', 'region': 'Ásia Central'},
            {'name': 'Arábia Saudita', 'name_en': 'Saudi Arabia', 'name_es': 'Arabia Saudita', 'code': 'SA', 'ddi': '+966', 'flag': 'sa', 'continent': 'Ásia', 'region': 'Oriente Médio'},
            {'name': 'Armênia', 'name_en': 'Armenia', 'name_es': 'Armenia', 'code': 'AM', 'ddi': '+374', 'flag': 'am', 'continent': 'Ásia', 'region': 'Cáucaso'},
            {'name': 'Azerbaijão', 'name_en': 'Azerbaijan', 'name_es': 'Azerbaiyán', 'code': 'AZ', 'ddi': '+994', 'flag': 'az', 'continent': 'Ásia', 'region': 'Cáucaso'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 4/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 4 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part5')
