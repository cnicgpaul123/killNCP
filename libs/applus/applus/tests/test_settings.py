# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import unittest
from applus import settings


__all__ = ['TestSetting']


class TestSetting(unittest.TestCase):

    def test_settings(self):
        namespace = 'API'
        conf = settings.Settings(namespace)
        conf.extend({
            'NAME': 'Bob',
            'AGE': '13',
            'KLASS': 'datetime.timedelta',
            'PERIOD': 0,
            'IMPORT_PATH_ERR': 'datetimeinvalid.abc',
            'IMPORT_ATTR_ERR': 'datetime.timedeltainvalid',
        }, [
            'KLASS',
            'IMPORT_PATH_ERR',
            'IMPORT_ATTR_ERR',
        ], {
            'AGE': int,
            'PERIOD': 'datetime.timedelta',
        }, [
            'DEPRECATED',
        ])
        # test default
        self.assertEqual(conf.NAME, "Bob")
        self.assertEqual(conf.AGE, 13)
        self.assertEqual(conf.KLASS.__name__, 'timedelta')
        self.assertEqual(conf.PERIOD.__class__.__name__, 'timedelta')
        with self.assertRaises(AttributeError) as exc:
            str(conf.UNKNOWN)
        self.assertEqual(str(exc.exception), "Invalid API setting: 'UNKNOWN'")
        with self.assertRaises(ImportError) as exc:
            str(conf.IMPORT_PATH_ERR)
        self.assertEqual(str(exc.exception), (
            "Could not import 'datetimeinvalid.abc' "
            "for API setting 'IMPORT_PATH_ERR': doesn't look like a module path"))
        with self.assertRaises(ImportError) as exc:
            str(conf.IMPORT_ATTR_ERR)
        self.assertEqual(str(exc.exception), (
            "Could not import 'datetime.timedeltainvalid' "
            "for API setting 'IMPORT_ATTR_ERR': module doesn't define the attribute/class"))
        # extend
        with self.assertRaises(RuntimeError) as exc:
            conf.extend({'NAME': 'Eve'}, [], {}, [])
        self.assertEqual(str(exc.exception), (
            "The 'NAME' API setting has been registered, "
            "can not occur in 'DEFAULTS'."))
        with self.assertRaises(RuntimeError) as exc:
            conf.extend({}, ['PERIOD'], {}, [])
        self.assertEqual(str(exc.exception), (
            "The 'PERIOD' API setting has been registered, "
            "can not occur in 'IMPORT_STRINGS'."))
        with self.assertRaises(RuntimeError) as exc:
            conf.extend({}, [], {'IMPORT_PATH_ERR': str}, [])
        self.assertEqual(str(exc.exception), (
            "The 'IMPORT_PATH_ERR' API setting has been registered, "
            "can not occur in 'CLEAN_SETTINGS'."))
        with self.assertRaises(RuntimeError) as exc:
            conf.extend({}, [], {}, ['IMPORT_ATTR_ERR'])
        self.assertEqual(str(exc.exception), (
            "The 'IMPORT_ATTR_ERR' API setting has been registered, "
            "can not occur in 'REMOVED_SETTINGS'."))
        # update
        conf.update({"NAME": "Eve"}) # Do nothing
        self.assertEqual("Bob", conf.NAME)
        with self.assertRaises(RuntimeError) as exc:
            conf.update({"NAME": "Eve"})
        self.assertEqual(str(exc.exception), "The 'NAME' API setting has been set.")
        with self.assertRaises(RuntimeError) as exc:
            conf.update({"DEPRECATED": None})
        self.assertEqual(str(exc.exception), "The 'DEPRECATED' API setting has been removed.")
        conf.update({"EMAIL": "nobody@localhost"})
        #
