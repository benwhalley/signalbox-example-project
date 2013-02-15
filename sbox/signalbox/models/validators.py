import phonenumbers
from phonenumbers.phonenumberutil import number_type, is_possible_number
from django.contrib.humanize.templatetags.humanize import naturalday
from datetime import datetime
from django.core.exceptions import ValidationError
from django.conf import settings
from signalbox.phone_field import PhoneNumber
from django.utils.safestring import mark_safe
from naturaltimes import parse_natural_date

client = settings.TWILIOCLIENT


def valid_natural_datetime(value):
    output = "relative to now (%s) <pre>   "

    results, errors = zip(*[parse_natural_date(t) for t in value.splitlines()])

    if sum([bool(i) for i in errors if i]):
        raise ValidationError(", ".join([i for i in errors if i]))

    return value


def valid_hour(value):
    try:
        assert int(value) in range(0, 23)
        return value
    except AssertionError:
        raise ValidationError("Valid hours are between 0 and 23.")


def valid_hours_list(value):
    hours = value.split(",")
    try:
        _ = [valid_hour(i) for i in hours]
        return value
    except ValidationError as e:
        raise


def in_minute_range(value):
    if not 0 < value < 60:
        raise ValidationError("Enter a number from 0 to 59.")
    return value


def only_includes_allowed_fields(value):
    """Convert value to a list of possible userprofile field names
    and check they are in the list of possible fields which could
    be added for a study."""
    fields = value.split()
    for i in fields:
        if i not in settings.USER_PROFILE_FIELDS:
            raise ValidationError("{} not allowed".format(i))
    return value


def no_count_property_in_syntax(value):
    if "count=" in value:
        raise ValidationError(
            """`count' parameter found. Use `max_number_observations'.""")
    return value


def valid_twilio_sender_numbers():
    if not client:
        return ValidationError("No Twilio settings available")
    return [i.phone_number for i in client.caller_ids.list()]


def is_twilio_approved(value):
    if not client:
        return ValidationError("No Twilio settings available")
    if client.caller_ids.list(phone_number=value):
        return True
    else:
        valid_numbers = valid_twilio_sender_numbers()
        raise ValidationError("""This number is not validated as a CallerId with your Twilio account. Currently validated numbers are: %s.""" % (", ".join(valid_numbers)))


def date_in_past(value):
    """Return true if the date is before the present"""

    if value > datetime.now():
        raise ValidationError("This date can't be in the future.")


def is_24_hour(value):
    if 0 < value < 25:
        return True
    raise ValidationError('''Number must be between 1 and 24''')


def could_be_number(value):
    if is_possible_number(value) is False:
        raise ValidationError("Not a phone number")


def is_mobile_number(value):
    """Note, using phonenumbers lib, we allow for ambiguous numbers which could be mobiles in countries like USA."""
    try:
        assert number_type(value) in [1, 2]
    except AssertionError:
        raise ValidationError('''Not a mobile number.''')


def is_landline(value):
    try:
        assert number_type(value) is 0
    except AssertionError:
        raise ValidationError('''Not a landline number.''')


def is_number_from_study_area(value):
    try:
        tests = [value.country_code == i for i in settings.VALID_COUNTRY_CODES]
        assert sum(tests) > 0
    except AssertionError:
        raise ValidationError("Country code not allowed.")
