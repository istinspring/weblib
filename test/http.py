# coding: utf-8
from unittest import TestCase

from weblib.http import normalize_url

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
