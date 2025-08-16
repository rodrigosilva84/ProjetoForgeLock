from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 2/10)'

    def handle(self, *args, **options):
        # PARTE 2: Próximos 20 países (América do Sul e Europa)
        countries_data = [
            # América do Sul
            {'name': 'Argentina', 'name_en': 'Argentina', 'name_es': 'Argentina', 'code': 'AR', 'ddi': '+54', 'flag': 'ar', 'continent': 'América do Sul', 'region': 'Cone Sul'},
            {'name': 'Bolívia', 'name_en': 'Bolivia', 'name_es': 'Bolivia', 'code': 'BO', 'ddi': '+591', 'flag': 'bo', 'continent': 'América do Sul', 'region': 'Andina'},
            {'name': 'Brasil', 'name_en': 'Brazil', 'name_es': 'Brasil', 'code': 'BR', 'ddi': '+55', 'flag': 'br', 'continent': 'América do Sul', 'region': 'Brasil'},
            {'name': 'Chile', 'name_en': 'Chile', 'name_es': 'Chile', 'code': 'CL', 'ddi': '+56', 'flag': 'cl', 'continent': 'América do Sul', 'region': 'Cone Sul'},
            {'name': 'Colômbia', 'name_en': 'Colombia', 'name_es': 'Colombia', 'code': 'CO', 'ddi': '+57', 'flag': 'co', 'continent': 'América do Sul', 'region': 'Andina'},
            {'name': 'Equador', 'name_en': 'Ecuador', 'name_es': 'Ecuador', 'code': 'EC', 'ddi': '+593', 'flag': 'ec', 'continent': 'América do Sul', 'region': 'Andina'},
            {'name': 'Guiana', 'name_en': 'Guyana', 'name_es': 'Guyana', 'code': 'GY', 'ddi': '+592', 'flag': 'gy', 'continent': 'América do Sul', 'region': 'Caribe'},
            {'name': 'Paraguai', 'name_en': 'Paraguay', 'name_es': 'Paraguay', 'code': 'PY', 'ddi': '+595', 'flag': 'py', 'continent': 'América do Sul', 'region': 'Platina'},
            {'name': 'Peru', 'name_en': 'Peru', 'name_es': 'Perú', 'code': 'PE', 'ddi': '+51', 'flag': 'pe', 'continent': 'América do Sul', 'region': 'Andina'},
            {'name': 'Suriname', 'name_en': 'Suriname', 'name_es': 'Surinam', 'code': 'SR', 'ddi': '+597', 'flag': 'sr', 'continent': 'América do Sul', 'region': 'Caribe'},
            {'name': 'Uruguai', 'name_en': 'Uruguay', 'name_es': 'Uruguay', 'code': 'UY', 'ddi': '+598', 'flag': 'uy', 'continent': 'América do Sul', 'region': 'Cone Sul'},
            {'name': 'Venezuela', 'name_en': 'Venezuela', 'name_es': 'Venezuela', 'code': 'VE', 'ddi': '+58', 'flag': 've', 'continent': 'América do Sul', 'region': 'Caribe'},
            
            # Europa
            {'name': 'Albânia', 'name_en': 'Albania', 'name_es': 'Albania', 'code': 'AL', 'ddi': '+355', 'flag': 'al', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Andorra', 'name_en': 'Andorra', 'name_es': 'Andorra', 'code': 'AD', 'ddi': '+376', 'flag': 'ad', 'continent': 'Europa', 'region': 'Península Ibérica'},
            {'name': 'Áustria', 'name_en': 'Austria', 'name_es': 'Austria', 'code': 'AT', 'ddi': '+43', 'flag': 'at', 'continent': 'Europa', 'region': 'Europa Central'},
            {'name': 'Bélgica', 'name_en': 'Belgium', 'name_es': 'Bélgica', 'code': 'BE', 'ddi': '+32', 'flag': 'be', 'continent': 'Europa', 'region': 'Europa Ocidental'},
            {'name': 'Bielorrússia', 'name_en': 'Belarus', 'name_es': 'Bielorrusia', 'code': 'BY', 'ddi': '+375', 'flag': 'by', 'continent': 'Europa', 'region': 'Europa Oriental'},
            {'name': 'Bósnia e Herzegovina', 'name_en': 'Bosnia and Herzegovina', 'name_es': 'Bosnia y Herzegovina', 'code': 'BA', 'ddi': '+387', 'flag': 'ba', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Bulgária', 'name_en': 'Bulgaria', 'name_es': 'Bulgaria', 'code': 'BG', 'ddi': '+359', 'flag': 'bg', 'continent': 'Europa', 'region': 'Balcãs'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 2/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 2 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part3')
