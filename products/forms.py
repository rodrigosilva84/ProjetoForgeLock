from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product, Category, ProductImage, Scale, ProductType


class CategoryForm(forms.ModelForm):
    """Formulário para criação/edição de categorias"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome da categoria')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Descrição da categoria (opcional)')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Nome') + ' *'
        self.fields['description'].label = _('Descrição')
        self.fields['is_active'].label = _('Ativo')


class ProductForm(forms.ModelForm):
    """Formulário para criação/edição de produtos"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'product_type', 'category',
            'cost_price', 'sale_price', 'currency', 'stock_quantity',
            'scale', 'dimensions_x', 'dimensions_y', 'dimensions_z',
            'dimension_unit', 'weight', 'weight_unit', 'print_time_estimate'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome do produto')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Descrição do produto')
            }),
            'product_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'scale': forms.Select(attrs={
                'class': 'form-select'
            }),
            'dimensions_x': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'dimensions_y': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'dimensions_z': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'dimension_unit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'weight_unit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'print_time_estimate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('ex: 2:30')
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels traduzidos
        self.fields['name'].label = _('Nome') + ' *'
        self.fields['description'].label = _('Descrição')
        self.fields['product_type'].label = _('Tipo') + ' *'
        self.fields['category'].label = _('Categoria')
        self.fields['cost_price'].label = _('Preço de Custo')
        self.fields['sale_price'].label = _('Preço de Venda')
        self.fields['currency'].label = _('Moeda') + ' *'
        self.fields['stock_quantity'].label = _('Quantidade em Estoque')
        self.fields['scale'].label = _('Escala')
        self.fields['dimensions_x'].label = _('Largura')
        self.fields['dimensions_y'].label = _('Altura')
        self.fields['dimensions_z'].label = _('Profundidade')
        self.fields['dimension_unit'].label = _('Unidade de Dimensão')
        self.fields['weight'].label = _('Peso')
        self.fields['weight_unit'].label = _('Unidade de Peso')
        self.fields['print_time_estimate'].label = _('Tempo de Impressão')
        
        # Definir valores padrão para campos obrigatórios
        if not self.instance.pk:  # Apenas para novos produtos
            self.fields['dimension_unit'].initial = 'cm'
            self.fields['weight_unit'].initial = 'g'
            
        # Garantir que os campos tenham valores padrão mesmo sem dados POST
        if not self.data:
            if not self.fields['dimension_unit'].initial:
                self.fields['dimension_unit'].initial = 'cm'
            if not self.fields['weight_unit'].initial:
                self.fields['weight_unit'].initial = 'g'

    def clean_print_time_estimate(self):
        """Validação do formato HH:MM"""
        time = self.cleaned_data.get('print_time_estimate')
        if time:
            try:
                hours, minutes = time.split(':')
                int(hours)
                int(minutes)
                if int(minutes) >= 60:
                    raise forms.ValidationError(_('Minutos devem ser menores que 60'))
            except (ValueError, AttributeError):
                raise forms.ValidationError(_('Formato inválido. Use HH:MM (ex: 2:30)'))
        return time


class ProductImageForm(forms.ModelForm):
    """Formulário para edição de imagens de produto"""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary', 'order_index']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order_index': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = _('Imagem')
        self.fields['is_primary'].label = _('Imagem Principal')
        self.fields['order_index'].label = _('Ordem') 


class ProductTypeForm(forms.ModelForm):
    """Formulário para criação/edição de tipos de produto"""
    
    class Meta:
        model = ProductType
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome do tipo de produto')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Descrição do tipo de produto (opcional)')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Nome') + ' *'
        self.fields['description'].label = _('Descrição')
        self.fields['is_active'].label = _('Ativo')


class ScaleForm(forms.ModelForm):
    """Formulário para criação/edição de escalas"""
    
    class Meta:
        model = Scale
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome da escala (ex: 1:100)')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Descrição da escala (opcional)')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Nome') + ' *'
        self.fields['description'].label = _('Descrição')
        self.fields['is_active'].label = _('Ativo') 


class CountryForm(forms.ModelForm):
    """Formulário para edição de países"""
    
    class Meta:
        model = None  # Será definido dinamicamente
        fields = ['name', 'name_en', 'name_es', 'is_active', 'flag']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome do país em português')
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome do país em inglês')
            }),
            'name_es': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome do país em espanhol')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'flag': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Nome (Português)') + ' *'
        self.fields['name_en'].label = _('Nome (Inglês)')
        self.fields['name_es'].label = _('Nome (Espanhol)')
        self.fields['is_active'].label = _('Ativo')
        self.fields['flag'].label = _('Bandeira')
        self.fields['flag'].required = False 