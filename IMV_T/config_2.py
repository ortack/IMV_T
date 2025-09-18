import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1","localhost","192.168.1.250","imv.ortack.com"]

#CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000','https://127.0.0.1:8000','http://imv.ortack.com','https://imv.ortack.com']
#CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:8000','https://127.0.0.1:8000','http://imv.ortack.com','https://imv.ortack.com']
#Para imv.ortack.com
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000','https://127.0.0.1:8000','http://imv.ortack.com','https://imv.ortack.com',]
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:8000','https://127.0.0.1:8000','http://imv.ortack.com','https://imv.ortack.com',]

WSGI_APPLICATION = 'IMV_T.wsgi.application'
ASGI_APPLICATION = 'IMV_T.asgi.application'



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE = {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'imv_t',
        'USER': 'root',
        'PASSWORD': 'X23ab!11',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3307',
}

DATABASE_old = {
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
