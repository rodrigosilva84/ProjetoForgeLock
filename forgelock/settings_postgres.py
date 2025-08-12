"""
Configuração temporária para migração SQLite → PostgreSQL
"""
import os
from pathlib import Path
from .settings import *

# Configuração específica para PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'forgelock_db',
        'USER': 'forgelock_user',
        'PASSWORD': 'forgelock_password',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

# Manter outras configurações do settings.py original
