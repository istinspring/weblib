import warnings


class WeblibError(Exception):
    """
    Base class for all custom exceptions
    defined in weblib package.
    """


class DataNotFound(WeblibError, IndexError):
    """
    Raised when it is not possible to find requested
    data.
    """


class RuntimeConfigError(WeblibError):
    """
    Raised when passed parameters do not makes sense
    or conflict with something.
    """


def warn(msg):
    warnings.warn(msg, category=GrabDeprecationWarning, stacklevel=3)
