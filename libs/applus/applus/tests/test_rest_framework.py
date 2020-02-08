# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,protected-access
import unittest
from applus.rest_framework import routers


__all__ = ['TestRouter']


class TestRouter(unittest.TestCase):

    def test_filter(self):
        router = routers.FilterRouter()
        self.assertEqual(
            router._support_mapping_keys,
            ['create', 'destroy', 'list', 'partial_update', 'retrieve', 'update'])
        #
        self.assertEqual(router._convert_actions('LCR'),
                         ['l', 'c', 'r'])
        self.assertEqual(router._convert_actions('Li Cr Re'),
                         ['li', 'cr', 're'])
        self.assertEqual(router._convert_actions('Li|Cr|Re'),
                         ['li', 'cr', 're'])
        #
        methods = ['list', 'create', 'retrieve']
        self.assertEqual(router._get_methods('LCR'), methods)
        self.assertEqual(router._get_methods('Li Cr Re'), methods)
        self.assertEqual(router._get_methods('Li|Cr|Re'), methods)
        self.assertEqual(router._get_methods(('Li', 'Cr', 'Re')), methods)
        #
        viewset = 1
        router._set_bind_actions(viewset, None, None)
        self.assertNotIn(viewset, router.exclude_method_map)
        #
        viewset += 1
        #
