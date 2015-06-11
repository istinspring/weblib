# coding: utf-8
from unittest import TestCase
from six.moves.urllib.parse import quote

from weblib.http import normalize_url, RESERVED_CHARS

class HttpTestCase(TestCase):
    def test_normalize_url_idn(self):
        url = 'http://почта.рф/path?arg=val'
        norm_url = 'http://xn--80a1acny.xn--p1ai/path?arg=val'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_unicode_path(self):
        url = u'https://ru.wikipedia.org/wiki/Россия'
        norm_url = 'https://ru.wikipedia.org/wiki'\
                   '/%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_unicode_query(self):
        url = 'https://ru.wikipedia.org/w/index.php?title=Заглавная_страница'
        norm_url = 'https://ru.wikipedia.org/w/index.php'\
                   '?title=%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD'\
                   '%D0%B0%D1%8F_%D1%81%D1%82%D1%80'\
                   '%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_with_mix_of_norm_and_unnorm(self):
        url = 'http://test.com/!?%21'
        norm_url = 'http://test.com/!?%21'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_normalized_ascii(self):
        url = 'http://test.com/%21?%21'
        norm_url = 'http://test.com/%21?%21'
        self.assertEqual(norm_url, normalize_url(url))


    def test_normalize_normalized_non_ascii(self):
        url = 'http://www.film.ru/movies/a-z/%D0%9F?%d0%9f'
        norm_url = 'http://www.film.ru/movies/a-z/%D0%9F?%d0%9f'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_non_quoted_percent(self):
        url = 'http://test.com/%9z%21'
        norm_url = 'http://test.com/%9z%21'
        self.assertEqual(norm_url, normalize_url(url))

    def test_quoted_query_in_query(self):
        url = (u"https://graph.facebook.com/fql?q=SELECT%20url%20,total_count"
               u"%20FROM%20link_stat%20WHERE%20url%20in%20('http%3A%2F%2F"
               u"www.ksl.com%2F%3Fsid%3D34840696%26nid%3D148')")
        #norm_url = ("https://graph.facebook.com/fql?q=SELECT%20url%20%2C"
        #            "total_count%20FROM%20link_stat%20WHERE%20url%20in"
        #            "%20%28%27http%3A%2F%2Fwww.ksl.com%2F%3Fsid%3D"
        #            "34840696%26nid%3D148%27%29")
        self.assertEqual(url, normalize_url(url))

    def test_reserved_delims(self):
        path = RESERVED_CHARS.replace('/', '')
        query = RESERVED_CHARS.replace('?', '')
        fragment = RESERVED_CHARS.replace('#', '')
        url = 'http://domain.com/%s?%s#%s' % (path, query, fragment)
        self.assertEqual(url, normalize_url(url))
