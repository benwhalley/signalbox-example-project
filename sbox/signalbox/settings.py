# Django

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-uk'
USE_I18N = False
USE_L10N = False


DATE_INPUT_FORMATS = ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%b %d %Y',
                      '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
                      '%B %d, %Y', '%d %B %Y', '%d %B, %Y')

DATETIME_INPUT_FORMATS = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d',
                          '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y',
                          '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%d/%m/%y')


# TWILIO #
TTS_VOICE = 'female'
TTS_LANGUAGE = 'en-gb'
DEFAULT_TELEPHONE_COUNTRY_CODE = "GB"  # determines numbers format on input
VALID_COUNTRY_CODES = [44, ]  # only numbers from here are allowed for users
ENABLE_ANSWER_PHONE = False

# To enable recording of answerphone messages uncomment these lines:
# ENABLE_ANSWER_PHONE = True
# ANSWER_PHONE_MESSAGE = """Hi, this is the automated study telephone line. If
# you'd like to speak to someone about the study please call 023 8 0 5 9 5 0 7 7.
# That's  023 8 0 5 9 5 0 7 7. Thanks. Goodbye."""
# ANSWER_PHONE_MESSAGE_THANKS = """Thanks. We'll be in touch soon. Goodbye."""


# SIGNALBOX

# this logs users in when they click a link in an email... see start_data-entry()
LOGIN_FROM_OBSERVATION_TOKEN = False

SHOW_USER_CURRENT_STUDIES = False

MY_SITE_PROTOCOL = "http"
MY_SITE_PORT = 80


USER_PROFILE_FIELDS = [
    # this is the list of possible fields in the user profile
    # list in the order in which they should appear in the form
    # note, you can't simply add fields here - they must also be
    # defined on the UserProfile model.
    'landline',
    'mobile',
    'site',
    'address_1',
    'address_2',
    'address_3',
    'county',
    'postcode',
]


DEFAULT_USER_PROFILE_FIELDS = [
    # list fields required for all studies
    'postcode',
]

OB_DATA_TYPES = [
                    ('external_id', "External reference number, e.g. a Twilio SID"),
                    ('attempt', "Attempt"),
                    ('reminder', "Reminder"),
                    ('success', "Success"),
                    ('failure', "Failure"),
                    ('timeshift', "Timeshift"),
                ]
OB_DATA_TYPES_DICT = dict(OB_DATA_TYPES)

STATUS_CHOICES_DICT = {
                    0: "pending",
                   -2: "email sent, response pending",
                   -3: "due, awaiting completion",
                   -1: "in progress",
                    1: "complete",
                  -99: "failed"
                  }
STATUS_CHOICES = sorted(zip(STATUS_CHOICES_DICT.keys(), STATUS_CHOICES_DICT.values()), reverse=True)

# Could be expanded in future for minimization, etc.
ALLOCATION_CHOICES = (
                        ("random", "Weighted random" ),
                        ( "balanced_groups_adaptive_randomisation", "Adaptive (weighted) randomisation to balance conditions" )
                     )

SMS_STATUSCODES = {
     'd': ('delivered', True),
     'f': ('failed', False),
     'e': ('error', False),
     'j': ('', False),
     'u': ('', False)
}

TITLE_CHOICES = [ (i,i) for i in ['', 'Mr', 'Mrs', 'Ms', 'Miss', 'Dr', 'Prof', 'Rev',] ]

