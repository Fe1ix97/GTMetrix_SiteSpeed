import re

import six
from gtmetrix import settings
from gtmetrix.exceptions import (GTmetrixAPIKeyIsNone,
                                 GTmetrixEmailIsNone,
                                 GTmetrixEmailIsNotStringtype,
                                 GTmetrixInvalidEmail,
                                 GTmetrixAPIUrlIsNone,
                                 GTmetrixBadAPIUrl)

__all__ = ['validate_email',
           'validate_api_key',
           'validate_api_url']

# Snagged from: https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script
email_re = re.compile(
    '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(''\.[a-z]{2,''4})$')


def validate_email(email):
    """Check for valid email address, raise correct exception if not."""
    if email is None:
        raise GTmetrixEmailIsNone

    if not isinstance(email, six.string_types):
        raise GTmetrixEmailIsNotStringtype

    if email_re.match(email) is None:
        raise GTmetrixInvalidEmail

    return True


def validate_api_key(key):
    """Check for valid API key.  Stubbed out for now."""
    if key is None:
        raise GTmetrixAPIKeyIsNone
    return True


def validate_api_url(url):
    """Ensure that it's set to what it was when settings.py was written.

    Prevents e.g. testing api/0.1 calls against api/1.0 if it ever comes
    out."""
    if url is None:
        raise GTmetrixAPIUrlIsNone

    if url != settings.good_url:
        raise GTmetrixBadAPIUrl

    return True
