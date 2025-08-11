from django.utils.translation import gettext_lazy as _


# Traduções para tipos de produto
PRODUCT_TYPE_TRANSLATIONS = {
    'STL': {
        'pt': 'STL',
        'en': 'STL',
        'es': 'STL',
    },
    'Modelo Físico': {
        'pt': 'Modelo Físico',
        'en': 'Physical Model',
        'es': 'Modelo Físico',
    },
    'Serviço': {
        'pt': 'Serviço',
        'en': 'Service',
        'es': 'Servicio',
    },
}

# Traduções para categorias
CATEGORY_TRANSLATIONS = {
    'Action Figures': {
        'pt': 'Figuras de Ação',
        'en': 'Action Figures',
        'es': 'Figuras de Acción',
    },
    'Decoração': {
        'pt': 'Decoração',
        'en': 'Decoration',
        'es': 'Decoración',
    },
    'Dioramas': {
        'pt': 'Dioramas',
        'en': 'Dioramas',
        'es': 'Dioramas',
    },
    'Ferramentas': {
        'pt': 'Ferramentas',
        'en': 'Tools',
        'es': 'Herramientas',
    },
    'Gospel': {
        'pt': 'Evangélico',
        'en': 'Gospel',
        'es': 'Evangélico',
    },
    'Modelagem': {
        'pt': 'Modelagem',
        'en': 'Modeling',
        'es': 'Modelado',
    },
    'Outros': {
        'pt': 'Outros',
        'en': 'Others',
        'es': 'Otros',
    },
    'RPG': {
        'pt': 'RPG',
        'en': 'RPG',
        'es': 'RPG',
    },
    'Ímãs de Geladeira': {
        'pt': 'Ímãs de Geladeira',
        'en': 'Refrigerator Magnets',
        'es': 'Imanes de Refrigerador',
    },
}


def get_translated_name(original_name, language_code, translations_dict):
    """Retorna o nome traduzido baseado no idioma"""
    if original_name in translations_dict:
        return translations_dict[original_name].get(language_code, original_name)
    return original_name


def get_product_type_translation(name, language_code):
    """Retorna a tradução do tipo de produto"""
    return get_translated_name(name, language_code, PRODUCT_TYPE_TRANSLATIONS)


def get_category_translation(name, language_code):
    """Retorna a tradução da categoria"""
    return get_translated_name(name, language_code, CATEGORY_TRANSLATIONS) 