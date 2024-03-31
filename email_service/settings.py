SECRET_KEY = 'rg13hdq!v*awc_)+%)z1y2mv&aa8b4&42u)b2*eagkoba)^+$n'
DEBUG = True

INSTALLED_APPS = (
    'email_service',
    'corsheaders',  # pip install django-cors-headers
)


ROOT_URLCONF = 'email_service.urls'

MY_DOMAINS = ['wojciklaw.ca', 'sandrako.ca', 'infinite-auto.ca']


# Generate CORS_ALLOWED_ORIGINS with http, https schemes and www.
CORS_ALLOWED_ORIGINS = []
for domain in MY_DOMAINS:
    http_origin = f'http://{domain}'
    https_origin = f'https://{domain}'
    www_http_origin = f'http://www.{domain}'
    www_https_origin = f'https://www.{domain}'
    CORS_ALLOWED_ORIGINS.extend([http_origin, https_origin, www_http_origin, www_https_origin])

if DEBUG:
    CORS_ALLOWED_ORIGINS += ['http://localhost:63342', ]  # For testing

CORS_ALLOW_METHODS = [
    # 'DELETE',
    # 'GET',
    # 'OPTIONS',
    # 'PATCH',
    'POST',
    # 'PUT',
]

ALLOWED_USER_AGENTS = ['Mozilla', 'Chrome', 'Safari', 'Edge', 'Opera']

MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',
    # ...
]



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # Set the desired logging level here
    },
}

# Grab local settings
try:
    # from email_service.local_settings import GOOGLE_EMAIL
    # from email_service.local_settings import GOOGLE_EMAIL_APP_PASSWORD
    from email_service.local_settings import *  # NOQA
except ImportError:
    pass
