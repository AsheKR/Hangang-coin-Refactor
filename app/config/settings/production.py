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
    '.amazon.com',
]

sentry_sdk.init(
    dsn="https://925b7abfc0b74ef9bc6d3175516974a9@sentry.io/1372674",
    integrations=[DjangoIntegration()]
)

# Health Check 도메인을 허용하는 코드
EC2_PRIVATE_IP = None

try:
    resp = requests.get('http://169.254.170.2/v2/metadata')
    data = resp.json()
    # print(data)

    container_name = os.environ.get('DOCKER_CONTAINER_NAME', None)
    search_results = [x for x in data['Containers'] if x['Name'] == container_name]

    if len(search_results) > 0:
        container_meta = search_results[0]
    else:
        # Fall back to the pause container
        container_meta = data['Containers'][0]

    EC2_PRIVATE_IP = container_meta['Networks'][0]['IPv4Addresses'][0]
except:
    # silently fail as we may not be in an ECS environment
    pass

if EC2_PRIVATE_IP:
    # Be sure your ALLOWED_HOSTS is a list NOT a tuple
    # or .append() will fail
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

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