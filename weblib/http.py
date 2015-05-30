try:
    import urllib.parse as urllib
except ImportError:
    import urllib
from six.moves.urllib.parse import urlsplit, urlunsplit, quote, unquote
import re
import logging
import six

from weblib.error import RuntimeConfigError
from weblib.encoding import make_str, make_unicode, decode_pairs

from weblib.py3k_support import *

# I do not know, what the hell is going on, but sometimes
# when IDN url should be requested grab fails with error
# LookupError: unknown encoding: punycode
# That happens in grab/base.py near by 347 line on the line::
# kwargs['url'] = normalize_url(kwargs['url'])
# If you try to catch the error with except and import pdb; pdb.set_trace()
# then you'll get "no pdb module" error. WTF??
# But if you import pdb at the top of the module then you can use it
# So.... I import here this module and I hope that will helps
# My idea is that some mystical shit does some thing that breaks python
# environment,, breaks sys.path So, when special case occurs and some new module
# is need to be imported then that can't be done due to the unknown magical influence
import encodings.punycode

logger = logging.getLogger('weblib.http')
RE_NON_ASCII = re.compile(r'[^-.a-zA-Z0-9]')
RE_NOT_SAFE_URL = re.compile(r'[^-.:/?&;#a-zA-Z0-9]')


def urlencode(*args, **kwargs):
    logger.debug('Method weblib.http.urlencode is deprecated. '
                 'Please use weblib.http.smart_urlencode')
    return smart_urlencode(*args, **kwargs)


def smart_urlencode(items, charset='utf-8'):
    """
    Convert sequence of items into bytestring which could be submitted
    in POST or GET request.

    It differs from ``urllib.urlencode`` in that it can process unicode
    and some special values.

    ``items`` could dict or tuple or list.
    """

    if isinstance(items, dict):
        items = items.items()
    return urllib.urlencode(normalize_http_values(items, charset=charset))


def encode_cookies(items, join=True, charset='utf-8'):
    """
    Serialize dict or sequence of two-element items into string suitable
    for sending in Cookie http header.
    """

    def encode(val):
        """
        URL-encode special characters in the text.

        In cookie value only ",", " ", "\t" and ";" should be encoded
        """

        return val.replace(b' ', b'%20').replace(b'\t', b'%09')\
                  .replace(b';', b'%3B').replace(b',', b'%2C')

    if isinstance(items, dict):
        items = items.items()
    items = normalize_http_values(items, charset=charset)

    # py3 hack
    #if PY3K:
    #    items = decode_pairs(items, charset)

    tokens = []
    for key, value in items:
        tokens.append(b'='.join((encode(key), encode(value))))
    if join:
        return b'; '.join(tokens)
    else:
        return tokens


def normalize_http_values(items, charset='utf-8', ignore_classes=None):
    """
    Accept sequence of (key, value) paris or dict and convert each
    value into bytestring.

    Unicode is converted into bytestring using charset of previous response
    (or utf-8, if no requests were performed)

    None is converted into empty string. 

    If `ignore_classes` is not None and the value is instance of
    any classes from the `ignore_classes` then the value is not
    processed and returned as-is.
    """

    if isinstance(items, dict):
        items = items.items()

    def process(item):
        key, value = item

        if ignore_classes and isinstance(value, ignore_classes):
            pass
        elif isinstance(value, unicode):
            value = normalize_unicode(value, charset=charset)
        elif value is None:
            value = ''
        else:
            value = str(value)

        if isinstance(key, unicode):
            key = normalize_unicode(key, charset=charset)

        return key, value

    items =  list(map(process, items))
    #items = sorted(items, key=lambda x: x[0])
    return items


def normalize_unicode(value, charset='utf-8'):
    """
    Convert unicode into byte-string using detected charset (default or from
    previous response)

    By default, charset from previous response is used to encode unicode into
    byte-string but you can enforce charset with ``charset`` option
    """

    if not isinstance(value, unicode):
        return value
    else:
        #raise RuntimeConfigError('normalize_unicode function accepts only unicode values')
        return value.encode(charset, 'ignore')


def normalize_url(url):
    # The idea is to quick check that URL contains only safe chars
    # If whole URL is safe then there is no need to extract hostname part
    # and check if it is IDN

    # see details in RFC 2396
    url = make_unicode(url)
    if RE_NOT_SAFE_URL.search(url):
        parts = list(urlsplit(url))
        # Scheme
        pass
        # Hostname
        if RE_NON_ASCII.search(parts[1]):
            parts[1] = parts[1].encode('idna')
        # Path
        # use make_str because python2's `quote` can't handle unicode
        data = make_str(parts[2]) if six.PY2 else parts[2]
        parts[2] = quote(unquote(data), safe='/')
        # Query
        # use make_str because python2's `quote` can't handle unicode
        data = make_str(parts[3]) if six.PY2 else parts[3]
        parts[3] = quote(unquote(data), safe='&=')

        return urlunsplit(map(make_unicode, parts))
    return url


def normalize_post_data(data, charset):
    if isinstance(data, basestring):
        # bytes-string should be posted as-is
        # unicode should be converted into byte-string
        if isinstance(data, unicode):
            return normalize_unicode(data, charset)
        else:
            return data
    else:
        # dict, tuple, list should be serialized into byte-string
        return smart_urlencode(data, charset)
