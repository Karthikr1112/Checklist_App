from .base import *  # noqa

DEBUG = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# IMPORTANT: Tell Django it's served under /fin
FORCE_SCRIPT_NAME = "/cl"

# Cookie paths
SESSION_COOKIE_PATH = '/cl/'
CSRF_COOKIE_PATH = '/cl/'

# Unique cookie names
SESSION_COOKIE_NAME = 'cl_sessionid'
CSRF_COOKIE_NAME = 'cl_csrftoken'

CSRF_TRUSTED_ORIGINS = [
    "https://jeyarama.com",
    "https://www.jeyarama.com",
]
