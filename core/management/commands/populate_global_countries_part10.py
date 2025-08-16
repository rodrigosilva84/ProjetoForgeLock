from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Popula países globais com informações de continente e região (Parte 10/10 - FINAL)'

    def handle(self, *args, **options):
        # PARTE 10: Final da África e territórios especiais
        countries_data = [
            # África (final)
            {'name': 'Serra Leoa', 'name_en': 'Sierra Leone', 'name_es': 'Sierra Leona', 'code': 'SL', 'ddi': '+232', 'flag': 'sl', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Somália', 'name_en': 'Somalia', 'name_es': 'Somalia', 'code': 'SO', 'ddi': '+252', 'flag': 'so', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Sudão', 'name_en': 'Sudan', 'name_es': 'Sudán', 'code': 'SD', 'ddi': '+249', 'flag': 'sd', 'continent': 'África', 'region': 'África do Norte'},
            {'name': 'Sudão do Sul', 'name_en': 'South Sudan', 'name_es': 'Sudán del Sur', 'code': 'SS', 'ddi': '+211', 'flag': 'ss', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Tanzânia', 'name_en': 'Tanzania', 'name_es': 'Tanzania', 'code': 'TZ', 'ddi': '+255', 'flag': 'tz', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Togo', 'name_en': 'Togo', 'name_es': 'Togo', 'code': 'TG', 'ddi': '+228', 'flag': 'tg', 'continent': 'África', 'region': 'África Ocidental'},
            {'name': 'Tunísia', 'name_en': 'Tunisia', 'name_es': 'Túnez', 'code': 'TN', 'ddi': '+216', 'flag': 'tn', 'continent': 'África', 'region': 'África do Norte'},
            {'name': 'Uganda', 'name_en': 'Uganda', 'name_es': 'Uganda', 'code': 'UG', 'ddi': '+256', 'flag': 'ug', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Zâmbia', 'name_en': 'Zambia', 'name_es': 'Zambia', 'code': 'ZM', 'ddi': '+260', 'flag': 'zm', 'continent': 'África', 'region': 'África Oriental'},
            {'name': 'Zimbábue', 'name_en': 'Zimbabwe', 'name_es': 'Zimbabue', 'code': 'ZW', 'ddi': '+263', 'flag': 'zw', 'continent': 'África', 'region': 'África Austral'},
            
            # Territórios especiais e dependências
            {'name': 'Groenlândia', 'name_en': 'Greenland', 'name_es': 'Groenlandia', 'code': 'GL', 'ddi': '+299', 'flag': 'gl', 'continent': 'América do Norte', 'region': 'América Anglo-Saxônica'},
            {'name': 'Hong Kong', 'name_en': 'Hong Kong', 'name_es': 'Hong Kong', 'code': 'HK', 'ddi': '+852', 'flag': 'hk', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Macau', 'name_en': 'Macau', 'name_es': 'Macao', 'code': 'MO', 'ddi': '+853', 'flag': 'mo', 'continent': 'Ásia', 'region': 'Ásia Oriental'},
            {'name': 'Porto Rico', 'name_en': 'Puerto Rico', 'name_es': 'Puerto Rico', 'code': 'PR', 'ddi': '+1', 'flag': 'pr', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Guam', 'name_en': 'Guam', 'name_es': 'Guam', 'code': 'GU', 'ddi': '+1', 'flag': 'gu', 'continent': 'Oceania', 'region': 'Micronésia'},
            {'name': 'Ilhas Marianas do Norte', 'name_en': 'Northern Mariana Islands', 'name_es': 'Islas Marianas del Norte', 'code': 'MP', 'ddi': '+1', 'flag': 'mp', 'continent': 'Oceania', 'region': 'Micronésia'},
            {'name': 'Ilhas Virgens Americanas', 'name_en': 'U.S. Virgin Islands', 'name_es': 'Islas Vírgenes de EE.UU.', 'code': 'VI', 'ddi': '+1', 'flag': 'vi', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Ilhas Virgens Britânicas', 'name_en': 'British Virgin Islands', 'name_es': 'Islas Vírgenes Británicas', 'code': 'VG', 'ddi': '+1', 'flag': 'vg', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Anguilla', 'name_en': 'Anguilla', 'name_es': 'Anguila', 'code': 'AI', 'ddi': '+1', 'flag': 'ai', 'continent': 'América do Norte', 'region': 'Caribe'},
            {'name': 'Montserrat', 'name_en': 'Montserrat', 'name_es': 'Montserrat', 'code': 'MS', 'ddi': '+1', 'flag': 'ms', 'continent': 'América do Norte', 'region': 'Caribe'},
        ]

        created_count = 0
        updated_count = 0
        
        self.stdout.write('🌍 Iniciando população de países globais (Parte 10/10 - FINAL)...')
        
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
            self.style.SUCCESS(f'🎉 PARTE 10 CONCLUÍDA! Total: {created_count} criados, {updated_count} atualizados')
        )
        self.stdout.write(f'📊 Total de países no sistema: {Country.objects.count()}')
        self.stdout.write('🎊 PARABÉNS! População global de países concluída com sucesso!')
        self.stdout.write('🌍 Agora você tem uma cobertura global completa com continentes e regiões!')
