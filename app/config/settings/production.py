from .base import *
import requests
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

PRODUCTION_JSON = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# 아마존에서 제공해주는 URL에 접속을 허용하는 코드
ALLOWED_HOSTS = [
    '.m41d.kr',
    '.amazonaws.com',
]

sentry_sdk.init(
    dsn="https://925b7abfc0b74ef9bc6d3175516974a9@sentry.io/1372674",
    integrations=[DjangoIntegration()]
)

# Health Check 도메인을 허용하는 코드
try:
    EC2_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').text
    ALLOWED_HOSTS.append(EC2_IP)
    ALLOWED_HOSTS.append('52.78.63.1')
    ALLOWED_HOSTS.append('13.209.46.98')
except requests.exceptions.RequestException:
    pass

STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

WSGI_APPLICATION = 'config.wsgi.production.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = PRODUCTION_JSON['DATABASES']

LOG_DIR = os.path.join(ROOT_DIR, '.log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(name)s (%(asctime)s)\n\t%(message)s',
        }
    },
    'handlers': {
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'formatter': 'default',
            # 최대 1MB를 넘게되면 새 파일을 만들어 저장
            'maxBytes': 1048576,
            # 최대 파일은 10개
            'backupCount': 10,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_error', 'console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}