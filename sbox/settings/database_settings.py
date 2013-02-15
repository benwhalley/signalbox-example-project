import dj_database_url
import os
from paths import *
from get_env_variable import get_env_variable

# a default
DB_URL = 'postgres://localhost/sbox'

# set to DATABASE_URL or fallback to sqlite
DATABASES = { 'default': dj_database_url.config(default=DB_URL) }



# if you really want to use sqlite:
# BASE, APPS = os.path.split(PROJECT_PATH)
# SQLITE_FILE = os.path.join(BASE, 'database', 'sbox.db')
# DB_URL = 'sqlite:////{}'.format(SQLITE_FILE)
