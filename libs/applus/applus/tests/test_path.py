# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import unittest
from applus import path


__all__ = ['TestPath']


class TestPath(unittest.TestCase):

    def _test_safe_url(self, origin, expect):
        self.assertEqual(expect, path.safe_url(origin))

    def test_safe_url(self):
        self._test_safe_url(
            'http://p05z0vref.bkt.clouddn.com/www/1532308938179_ul0848-7560_副本.jpg',
            'http://p05z0vref.bkt.clouddn.com/www/1532308938179_ul0848-7560_%E5%89%AF%E6%9C%AC.jpg')
