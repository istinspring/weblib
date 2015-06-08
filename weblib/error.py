import warnings
import logging


# WTF Grab doing here?
def warn(msg):
    warnings.warn(msg, category=GrabDeprecationWarning, stacklevel=3)


# ***********************************
# Base Classes to build Custom Errors
# ***********************************

class WeblibError(Exception):
    """
    Base class for all custom exceptions
    defined in weblib package.
    """

class ResponseNotValid(WeblibError):
    pass


# ********************
# Errors inside weblib
# ********************

class RuntimeConfigError(WeblibError):
    """
    Raised when passed parameters do not makes sense
    or conflict with something.
    """


# **********************
# Data Processing Errors
# **********************

class DataNotFound(WeblibError, IndexError):
    """
    Raised when it is not possible to find requested
    data.
    """


# *****************************
# ResponseNotValid based Classes
# *****************************

class DataNotValid(ResponseNotValid):
    pass


class RequestBanned(ResponseNotValid):
    pass


class CaptchaRequired(ResponseNotValid):
    pass


class PageNotFound(ResponseNotValid):
    pass


class AccessDenied(ResponseNotValid):
    pass


# *****************************
# ResponseNotValid based Classes
# specific to HTTP code errors
# *****************************

class HttpCodeNotValid(ResponseNotValid): 
    pass


class HttpCodeZero(HttpCodeNotValid):
    pass


# ********************
# Other Errors
# ********************
class NextPageNotFound(WeblibError):
    pass



# **********
# Deprecated
# **********
class CaptchaError(CaptchaRequired):
    def __init__(self, *args, **kwargs):
        logging.error('Class CaptchaError is deprecated. Use CaptchaRequired.')
        super(CaptchaError, self).__init__(*args, **kwargs)


class BanError(RequestBanned):
    def __init__(self, *args, **kwargs):
        logging.error('Class BanError is deprecated. Use RequestBanned.')
        super(BanError, self).__init__(*args, **kwargs)


class UnexpectedData(DataNotValid):
    def __init__(self, *args, **kwargs):
        logging.error('Class UnexpectedData is deprecated. Use DataNotValid.')
        super(UnexpectedData, self).__init__(*args, **kwargs)


class HttpCodeUnexpected(HttpCodeNotValid):
    def __init__(self, *args, **kwargs):
        logging.error('Class HttpCodeUnexpected is deprecated. '
                      'Use HttpCodeNotValid.')
        super(HttpCodeUnexpected, self).__init__(*args, **kwargs)


class UnexpectedContent(DataNotValid):
    def __init__(self, *args, **kwargs):
        logging.error('Class UnexpectedContent is deprecated. '
                      'Use DataNotValid.')
        super(UnexpectedContent, self).__init__(*args, **kwargs)
