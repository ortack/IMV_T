import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1","localhost"]



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_old = {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'imv',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3307',
}

DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'imv.sqlite3',
}


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_LOGGER = "django"
MSG_LOGGER = "tarjetas"

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'simple': {
			'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
		},
	},
	'handlers': {
		'file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': './logs/DJANGO_debug.log',
			'formatter': 'simple',
			'backupCount': 10, # keep at most 10 log files
			'maxBytes': 524288000 # 500MB
		},
	},
	'loggers': {
		DJANGO_LOGGER: {
			'handlers': ['file'],
			'level': 'WARNING',
			'propagate': True,
		},
		MSG_LOGGER: {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	},
}