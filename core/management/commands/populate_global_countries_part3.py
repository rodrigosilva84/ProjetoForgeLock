from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 3/10)'

    def handle(self, *args, **options):
        # PARTE 3: Mais países da Europa e início da Ásia
        countries_data = [
            # Europa (continuação)
            {'name': 'Croácia', 'name_en': 'Croatia', 'name_es': 'Croacia', 'code': 'HR', 'ddi': '+385', 'flag': 'hr', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Dinamarca', 'name_en': 'Denmark', 'name_es': 'Dinamarca', 'code': 'DK', 'ddi': '+45', 'flag': 'dk', 'continent': 'Europa', 'region': 'Escandinávia'},
            {'name': 'Eslováquia', 'name_en': 'Slovakia', 'name_es': 'Eslovaquia', 'code': 'SK', 'ddi': '+421', 'flag': 'sk', 'continent': 'Europa', 'region': 'Europa Central'},
            {'name': 'Eslovênia', 'name_en': 'Slovenia', 'name_es': 'Eslovenia', 'code': 'SI', 'ddi': '+386', 'flag': 'si', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Espanha', 'name_en': 'Spain', 'name_es': 'España', 'code': 'ES', 'ddi': '+34', 'flag': 'es', 'continent': 'Europa', 'region': 'Península Ibérica'},
            {'name': 'Estônia', 'name_en': 'Estonia', 'name_es': 'Estonia', 'code': 'EE', 'ddi': '+372', 'flag': 'ee', 'continent': 'Europa', 'region': 'Países Bálticos'},
            {'name': 'Finlândia', 'name_en': 'Finland', 'name_es': 'Finlandia', 'code': 'FI', 'ddi': '+358', 'flag': 'fi', 'continent': 'Europa', 'region': 'Escandinávia'},
            {'name': 'França', 'name_en': 'France', 'name_es': 'Francia', 'code': 'FR', 'ddi': '+33', 'flag': 'fr', 'continent': 'Europa', 'region': 'Europa Ocidental'},
            {'name': 'Grécia', 'name_en': 'Greece', 'name_es': 'Grecia', 'code': 'GR', 'ddi': '+30', 'flag': 'gr', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Hungria', 'name_en': 'Hungary', 'name_es': 'Hungría', 'code': 'HU', 'ddi': '+36', 'flag': 'hu', 'continent': 'Europa', 'region': 'Europa Central'},
            {'name': 'Irlanda', 'name_en': 'Ireland', 'name_es': 'Irlanda', 'code': 'IE', 'ddi': '+353', 'flag': 'ie', 'continent': 'Europa', 'region': 'Ilhas Britânicas'},
            {'name': 'Islândia', 'name_en': 'Iceland', 'name_es': 'Islandia', 'code': 'IS', 'ddi': '+354', 'flag': 'is', 'continent': 'Europa', 'region': 'Escandinávia'},
            {'name': 'Itália', 'name_en': 'Italy', 'name_es': 'Italia', 'code': 'IT', 'ddi': '+39', 'flag': 'it', 'continent': 'Europa', 'region': 'Europa Meridional'},
            {'name': 'Letônia', 'name_en': 'Latvia', 'name_es': 'Letonia', 'code': 'LV', 'ddi': '+371', 'flag': 'lv', 'continent': 'Europa', 'region': 'Países Bálticos'},
            {'name': 'Liechtenstein', 'name_en': 'Liechtenstein', 'name_es': 'Liechtenstein', 'code': 'LI', 'ddi': '+423', 'flag': 'li', 'continent': 'Europa', 'region': 'Europa Central'},
            {'name': 'Lituânia', 'name_en': 'Lithuania', 'name_es': 'Lituania', 'code': 'LT', 'ddi': '+370', 'flag': 'lt', 'continent': 'Europa', 'region': 'Países Bálticos'},
            {'name': 'Luxemburgo', 'name_en': 'Luxembourg', 'name_es': 'Luxemburgo', 'code': 'LU', 'ddi': '+352', 'flag': 'lu', 'continent': 'Europa', 'region': 'Europa Ocidental'},
            {'name': 'Macedônia do Norte', 'name_en': 'North Macedonia', 'name_es': 'Macedonia del Norte', 'code': 'MK', 'ddi': '+389', 'flag': 'mk', 'continent': 'Europa', 'region': 'Balcãs'},
            {'name': 'Malta', 'name_en': 'Malta', 'name_es': 'Malta', 'code': 'MT', 'ddi': '+356', 'flag': 'mt', 'continent': 'Europa', 'region': 'Europa Meridional'},
            {'name': 'Moldávia', 'name_en': 'Moldova', 'name_es': 'Moldavia', 'code': 'MD', 'ddi': '+373', 'flag': 'md', 'continent': 'Europa', 'region': 'Europa Oriental'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 3/10)...')
        
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
            self.style.SUCCESS(f'🎉 Parte 3 concluída! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('💡 Execute a próxima parte com: python manage.py populate_global_countries_part4')
