# coding: utf-8
from django.contrib.auth.models import User
from signalbox.models import Membership, Study, Observation
from signalbox.allocation import allocate

LONG_YUCKY_UNICODE = u"""Testing «ταБЬℓσ»: 1<2 & 4+1>3, now 20% off! ٩(-̮̮̃-̃)۶ ٩(●̮̮̃•̃)۶ ٩(͡๏̯͡๏)۶ ٩(-̮̮̃•̃).Bãｃòｎ ｉｐｓûｍ Ꮷｏｌòｒ ｓïｔ âｍêｔ òｃｃａéｃáｔ ｋïéｌｂäｓâ ｃåｐïｃｏｌà, ｃｈùｃｋ ｐｏｒｋ ｂéｌｌｙ íｎ àｌïｑûïｐ ｍéａｔｌòåｆ ｍòｌｌíｔ êｎíｍ ëｘ ｐｒòｓｃïüｔｔò âｎｄｏüｉｌｌｅ ｂèëｆ ｒíｂｓ. Eｘ ｓｔｒïｐ ｓｔｅａｋ ｐｏｒｋ ｌòｉｎ, ｓèｄ ｂｒëｓãｏｌá ｓｐèｃｋ ｏｃｃàｅｃâｔ ｔｏｎｇｕｅ. Iｄ ｐｒｏｓｃｉûｔｔｏ éｓｓé ｓｉｒｌòïｎ ëｔ òｆｆｉｃｉá ｌåｂｏｒìｓ ｆｒãｎｋｆúｒｔéｒ ｃａｐïｃòｌâ ｔｕｒｄúｃｋｅｎ. Qûïｓ ｔàｉｌ ｓｕｎｔ ｅìûｓｍòᏧ.
Tｈê Fｉｓｈ-Fòｏｔｍàｎ ｂｅｇａｎ ｂｙ ｐｒｏᏧüｃìｎｇ ｆｒòｍ ùｎᏧｅｒ ｈìｓ åｒｍ â ｇｒèàｔ ｌêｔｔëｒ, ｎèãｒｌｙ áｓ ｌåｒｇê ãｓ ｈｉｍｓéｌｆ, ãｎｄ ｔｈíｓ ｈè ｈäｎᏧêｄ ｏｖëｒ ｔｏ ｔｈè òｔｈëｒ, ｓａｙｉｎｇ, ïｎ á ｓｏｌｅｍｎ ｔｏｎé, 'Fòｒ ｔｈë Dùｃｈèｓｓ. Aｎ ìｎｖïｔàｔｉｏｎ ｆｒｏｍ ｔｈｅ Qｕèｅｎ ｔｏ ｐｌａｙ ｃｒòｑüｅｔ.' Tｈè Fｒòｇ-Fòｏｔｍàｎ ｒêｐｅàｔêｄ, íｎ ｔｈë ｓàｍè ｓòｌêｍｎ ｔｏｎｅ, ｏｎｌｙ ｃｈâｎｇìｎｇ ｔｈè ｏｒｄｅｒ òｆ ｔｈｅ ｗòｒｄｓ ã ｌｉｔｔｌè, 'Fｒòｍ ｔｈê Qｕééｎ. Aｎ ｉｎｖíｔåｔｉｏｎ ｆòｒ ｔｈｅ Dｕｃｈêｓｓ ｔｏ ｐｌàｙ ｃｒòｑｕｅｔ.'"""


QUESTIONNAIRE_POST_DATA = {
    'demo_shorttext': "abc", #LONG_YUCKY_UNICODE[:50],
    'demo_longtext': "abcdefg", #LONG_YUCKY_UNICODE,
    'demo_date': "2001-12-20",
    # 'demo_integer': "999",
    # 'demo_checkbox': ["1", "2"],
    'demo_list': "1",
    'demo_pulldown': "2",
    'demo_scale': "0",
    }

def setup_membership():
    """Create, allocate and add observations to a membership -> Membership """

    study = Study.objects.get(slug='test-study')
    user = make_user({'username': "TEST", 'email':"TEST@TEST.COM", 'password': "TEST"})
    membership = make_membership(study, user)
    allocate(membership)
    membership.add_observations()

    return membership


def make_user(details, profile_details=None):
    """Accept a dict of details and return a saved User object -> User.

    To make a user, require:
        - username
        - email
        - password

    Optionally allow a second dict containing fields for the UserProfile
    """

    password = details.pop('password')
    user = User(**details)
    user.set_password(password)
    user.save()

    if profile_details:
        profile = user.get_profile()
        [setattr(profile, k, v) for k,v in profile_details.items()]


    return user


def make_membership(study, user):
    """Take study and user -> Membership.
    """
    m = Membership(user=user, study=study)
    m.save()
    return m




