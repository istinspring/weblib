# coding: utf-8
from unittest import TestCase
import six
import warnings

from weblib.user_agent import random_user_agent

class HtmlUserAgent(TestCase):
    def test_it_works(self):
        self.assertTrue('Mozilla/5' in random_user_agent())

    def test_it_throwns_warning(self):
        with warnings.catch_warnings(record=True) as w:
            random_user_agent()
            self.assertEqual(1, len(w))
