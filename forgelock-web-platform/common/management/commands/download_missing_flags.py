from django.core.management.base import BaseCommand
from django.conf import settings
import os
import requests
from common.models import Country
import time

class Command(BaseCommand):
    help = 'Baixa bandeiras faltantes para todos os países'

    def handle(self, *args, **options):
        self.stdout.write('🚩 Iniciando download de bandeiras faltantes...')
        
        # Diretório das bandeiras
        flags_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'flags')
        os.makedirs(flags_dir, exist_ok=True)
        
        # Verificar bandeiras existentes
        existing_flags = set()
        if os.path.exists(flags_dir):
            for file in os.listdir(flags_dir):
                if file.endswith('.svg'):
                    existing_flags.add(file.replace('.svg', ''))
        
        self.stdout.write(f'📁 Bandeiras existentes: {len(existing_flags)}')
        
        # Obter países sem bandeiras
        countries_without_flags = Country.objects.filter(
            flag__isnull=False
        ).exclude(flag__in=existing_flags)
        
        self.stdout.write(f'🌍 Países sem bandeiras: {countries_without_flags.count()}')
        
        if not countries_without_flags.exists():
            self.stdout.write(self.style.SUCCESS('✅ Todas as bandeiras já estão presentes!'))
            return
        
        # API para bandeiras (FlagCDN)
        base_url = "https://flagcdn.com/w40/{}.svg"
        
        downloaded = 0
        failed = 0
        
        for country in countries_without_flags:
            flag_code = country.flag.lower()
            flag_url = base_url.format(flag_code)
            flag_path = os.path.join(flags_dir, f"{flag_code}.svg")
            
            try:
                self.stdout.write(f'⬇️  Baixando {country.name} ({flag_code})...')
                
                response = requests.get(flag_url, timeout=10)
                response.raise_for_status()
                
                with open(flag_path, 'wb') as f:
                    f.write(response.content)
                
                downloaded += 1
                self.stdout.write(f'✅ {country.name} baixado com sucesso')
                
                # Pausa para não sobrecarregar a API
                time.sleep(0.5)
                
            except Exception as e:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao baixar {country.name}: {str(e)}')
                )
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Download concluído! {downloaded} baixados, {failed} falharam')
        )
        self.stdout.write(f'📊 Total de bandeiras no sistema: {len(existing_flags) + downloaded}')
        
        # Executar collectstatic
        self.stdout.write('🔄 Executando collectstatic...')
        os.system('python manage.py collectstatic --noinput')
        self.stdout.write('✅ collectstatic concluído!')
