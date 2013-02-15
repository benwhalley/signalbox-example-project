from twilio.rest import TwilioRestClient
from get_env_variable import get_env_variable

SECRET_KEY = get_env_variable('SECRET_KEY')

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')

TWILIO_ID = get_env_variable('TWILIO_ID', required=False)
TWILIO_TOKEN = get_env_variable('TWILIO_TOKEN', required=False)

if TWILIO_ID and TWILIO_TOKEN:
    TWILIOCLIENT = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)
else:
    TWILIOCLIENT = None
