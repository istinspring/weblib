# coding: utf-8
from unittest import TestCase

from tools.html import find_refresh_url


class HtmlTestCase(TestCase):

    def test_find_refresh_url(self):
        url = find_refresh_url("""
            <meta http-equiv="refresh" content="5">
        """)
        self.assertEqual(None, url)

        url = find_refresh_url("""
            <meta http-equiv="refresh" content="5;URL='http://example.com/'">
        """)
        self.assertEqual('http://example.com/', url)

        url = find_refresh_url("""
            <meta http-equiv="refresh" content="0;URL='http://example.com/'">
        """)
        self.assertEqual('http://example.com/', url)

        url = find_refresh_url("""
            <meta http-equiv="refresh" content="5; url=http://example.com/">
        """)
        self.assertEqual('http://example.com/', url)

        url = find_refresh_url("""
            <meta http-equiv="refresh" content=" 0 ; url=http://example.com/">
        """)
        self.assertEqual('http://example.com/', url)
