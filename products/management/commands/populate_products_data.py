from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from products.models import ProductType, Category, Currency


class Command(BaseCommand):
    help = 'Popula dados de exemplo para produtos com traduções'

    def handle(self, *args, **options):
        self.stdout.write('Populando dados de produtos...')

        # Criar moedas
        currencies = [
            {'code': 'BRL', 'name': 'Real Brasileiro', 'symbol': 'R$'},
            {'code': 'USD', 'name': 'Dólar Americano', 'symbol': '$'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
        ]

        for currency_data in currencies:
            currency, created = Currency.objects.get_or_create(
                code=currency_data['code'],
                defaults=currency_data
            )
            if created:
                self.stdout.write(f'Moeda criada: {currency.code}')

        # Criar tipos de produto
        product_types = [
            {'name': 'STL', 'description': 'Arquivos 3D para impressão'},
            {'name': 'Modelo Físico', 'description': 'Produtos físicos impressos'},
            {'name': 'Serviço', 'description': 'Serviços de impressão 3D'},
        ]

        for type_data in product_types:
            product_type, created = ProductType.objects.get_or_create(
                name=type_data['name'],
                defaults=type_data
            )
            if created:
                self.stdout.write(f'Tipo de produto criado: {product_type.name}')

        # Criar categorias
        categories = [
            {'name': 'Action Figures', 'description': 'Figuras de ação'},
            {'name': 'Decoração', 'description': 'Itens decorativos'},
            {'name': 'Dioramas', 'description': 'Cenários e dioramas'},
            {'name': 'Ferramentas', 'description': 'Ferramentas e utilitários'},
            {'name': 'Gospel', 'description': 'Itens religiosos'},
            {'name': 'Modelagem', 'description': 'Modelos e miniaturas'},
            {'name': 'Outros', 'description': 'Outras categorias'},
            {'name': 'RPG', 'description': 'Itens para RPG'},
            {'name': 'Ímãs de Geladeira', 'description': 'Ímãs decorativos'},
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            if created:
                self.stdout.write(f'Categoria criada: {category.name}')

        self.stdout.write(
            self.style.SUCCESS('Dados de produtos populados com sucesso!')
        ) 