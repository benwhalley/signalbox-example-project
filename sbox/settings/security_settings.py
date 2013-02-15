
from get_env_variable import get_env_variable

SECURE_FRAME_DENY = True
SESSION_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = get_env_variable('SECURE_SSL_REDIRECT', required=False,
    default=False, int_to_bool=True)
