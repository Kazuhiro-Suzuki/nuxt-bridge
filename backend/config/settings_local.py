from .settings import *

SECRET_KEY = 'django-insecure-kv4y8crve9&!w9n-y*4c&lefia6h4nbe2%zydvls&7%@%gnell'
DEBUG = True
ALLOWED_HOSTS = ['*']
MIGRATION_MODULES = {
    'account': 'account.migrations.local',
    'app': 'app.migrations.local',
}
