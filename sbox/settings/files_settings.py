import os
from django.core.files.storage import FileSystemStorage
from get_env_variable import get_env_variable
from paths import *


AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME", default="signalbox-demo")
S3_URL = 'http://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

USER_UPLOAD_STORAGE_BACKEND = 'signalbox.s3.PrivateRootS3BotoStorage'
DEFAULT_FILE_STORAGE = STATICFILES_STORAGE = COMPRESS_STORAGE = 'signalbox.s3.CachedS3BotoStorage'

MEDIA_ROOT = os.path.join(PROJECT_PATH, "../files/media")
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, "../files/static")
STATIC_URL = S3_URL
ADMIN_MEDIA_PREFIX = S3_URL + 'admin/'

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = S3_URL


# # django_compressor
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

ALLOWED_UPLOAD_MIME_TYPES = [
    'application/pdf',
    'image/png',
    'image/jpeg',
    'image/gif',
]
