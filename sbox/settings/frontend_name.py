import string
from get_env_variable import get_env_variable

# load a customised frontend for the site
fe = get_env_variable('FRONTEND', required=False, default="frontend")
FRONTEND = str(fe)[:10]
assert set(FRONTEND).issubset(set(string.ascii_letters + "_-"))

