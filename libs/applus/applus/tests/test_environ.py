# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import os
import urllib
import unittest
from applus import environ


__all__ = ['TestEnviron']


class TestEnviron(unittest.TestCase):

    def test_environ(self):
        gef = environ.get_envfunc()
        # read default
        self.assertEqual(gef("SECRET_KEY", "AAAAFFFF"), "AAAAFFFF")
        self.assertEqual(gef("VERSION", 2, int), 2)
        self.assertEqual(gef("DEBUG", False, bool), False)
        # update env
        os.environ["SECRET_KEY"] = "BBBBEEEE"
        os.environ["VERSION"] = "3"
        os.environ["DEBUG"] = "true"
        # read environ
        self.assertEqual(gef("SECRET_KEY", "AAAAFFFF"), "BBBBEEEE")
        self.assertEqual(gef("VERSION", 2, int), 3)
        self.assertEqual(gef("DEBUG", False, bool), True)
        #
        self.assertEqual("x x", environ.decode_result("x%20x", "urllib.parse.unquote"))
        self.assertEqual("x x", environ.decode_result("x+x", "urllib.parse.unquote_plus"))
        self.assertEqual("x+x", environ.decode_result("x+x", "urllib.parse.unquote"))
        #

    DEF_DB_CONF = {
        "username": "root",
        "password": "",
        "hostname": "127.0.0.1",
        "port": 3306,
        "sql_mode": "STRICT_TRANS_TABLES",
    }

    def test_django_database(self):
        dbs = {}
        uri = "mysql:///db_sample"
        environ.update_django_db(dbs, 0, uri, **self.DEF_DB_CONF)
        self.assertEqual(dbs[0]["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(dbs[0]["USER"], "root")
        self.assertEqual(dbs[0]["PASSWORD"], "")
        self.assertEqual(dbs[0]["HOST"], "127.0.0.1")
        self.assertEqual(dbs[0]["PORT"], 3306)
        self.assertEqual(dbs[0]["NAME"], "db_sample")
        self.assertEqual(dbs[0]["OPTIONS"]["charset"], "utf8")
        self.assertEqual(dbs[0]["OPTIONS"]["sql_mode"], "STRICT_TRANS_TABLES")
        #
        uri = "mysql:///db_sample?charset=utf8mb4"
        environ.update_django_db(dbs, 0, uri, **self.DEF_DB_CONF)
        self.assertEqual(dbs[0]["OPTIONS"]["charset"], "utf8mb4")
        #
        uri = "mysql://@/db_sample"
        environ.update_django_db(dbs, 0, uri, **self.DEF_DB_CONF)
        self.assertEqual(dbs[0]["USER"], "root")
        self.assertEqual(dbs[0]["PASSWORD"], "")
        self.assertEqual(dbs[0]["HOST"], "127.0.0.1")
        self.assertEqual(dbs[0]["PORT"], 3306)
        #
        uri = "mysql://user:@/db_sample"
        environ.update_django_db(dbs, 0, uri, **self.DEF_DB_CONF)
        self.assertEqual(dbs[0]["USER"], "user")
        self.assertEqual(dbs[0]["PASSWORD"], "")
        #
        uri = "mysql://:pwd@/db_sample"
        environ.update_django_db(dbs, 0, uri, **self.DEF_DB_CONF)
        self.assertEqual(dbs[0]["USER"], "root")
        self.assertEqual(dbs[0]["PASSWORD"], "pwd")
        #
        uri = "mysql://@:8806/db_sample"
        environ.update_django_db(dbs, 0, uri, **self.DEF_DB_CONF)
        self.assertEqual(dbs[0]["HOST"], "127.0.0.1")
        self.assertEqual(dbs[0]["PORT"], 8806)
        # 密码中含有特殊字符：转义
        password = ":@#?;"
        quoted = urllib.parse.quote(password)
        uri = "mysql://username:{}@/db_sample".format(quoted)
        environ.update_django_db(dbs, 0, uri, **self.DEF_DB_CONF)
        self.assertEqual(dbs[0]["PASSWORD"], password)
        #

    def test_merge_uri(self):
        url = "http://u:p@localhost/db_sample?charset=utf8"
        parsed = environ.parse_uri(url)
        ret = environ.merge_uri(parsed, netloc="localhost")
        self.assertEqual(ret, "http://localhost/db_sample?charset=utf8")
        #

    def test_django_databases(self):
        mysql = "django.db.backends.mysql"
        sqlite3 = "django.db.backends.sqlite3"
        filename = "/path/to/db.sqlite3"
        mysql_opt = dict(sql_mode="")
        #
        dbs = {}
        environ.update_django_dbs(dbs, "")
        self.assertEqual({}, dbs)
        #
        dbs = {}
        environ.update_django_dbs(dbs, "file://"+filename)
        self.assertEqual(sqlite3, dbs["default"]["ENGINE"])
        self.assertEqual(filename, dbs["default"]["NAME"])
        #
        dbs = {}
        environ.update_django_dbs(dbs, "[]file://"+filename)
        self.assertEqual(filename, dbs["default"]["NAME"])
        #
        dbs = dict(default=dict(ENGINE=sqlite3, NAME=filename))
        environ.update_django_dbs(dbs, "[] [2nd]mysql://localhost/db_sample", **mysql_opt)
        self.assertEqual(sqlite3, dbs["default"]["ENGINE"])
        self.assertEqual(mysql, dbs["2nd"]["ENGINE"])
        #
