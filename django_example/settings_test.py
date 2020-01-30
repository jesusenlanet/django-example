try:
    from django_example.settings import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_example_database_test',
        'USER': 'django_example',
        'HOST': 'db',
        'PASSWORD': 'django_example',
        'PORT': 5432,
    }
}

FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'fixtures'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
