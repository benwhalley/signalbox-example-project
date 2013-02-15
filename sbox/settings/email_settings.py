import os
from get_env_variable import get_env_variable


if 'DATABASE_URL' in os.environ: # we are on heroku
  EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
  EMAIL_PORT = 465

  EMAIL_HOST = get_env_variable('EMAIL_HOST', required=False, default='email-smtp.us-east-1.amazonaws.com')
  EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', required=False)
  EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD', required=False)

else:
  EMAIL_HOST = 'localhost'
  EMAIL_PORT = 25
