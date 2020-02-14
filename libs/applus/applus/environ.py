# -*- coding: utf-8 -*-
""" 环境配置相关功能 """
import os
import urllib
from importlib import import_module


def get_envfunc(prefix=""):
    """ 允许指定配置前缀 """
    def wrapper(key, default, func=None):
        """ 读取环境配置并处理，支持默认值 """
        env_key = prefix + key
        if env_key not in os.environ:
            return default
        env_val = os.environ.get(env_key)
        if not func:
            return env_val
        if func is bool:
            return env_val.lower() in ["true"]
        return func(env_val)
    return wrapper


def decode_result(result, method='urllib.parse.unquote_plus'):
    """ 转义处理

    参考: https://api.mongodb.com/python/current/api/pymongo/mongo_client.html

        uri = "mongodb://%s:%s@%s" % (
            quote_plus(user), quote_plus(password), host)

        uri = "mongodb://%s:%s@%s" % (
            quote_plus(user), quote_plus(password), quote_plus(socket_path))
    """
    if not result or not method:
        return result
    if isinstance(method, str):
        module_path, class_name = method.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)(result)
    return method(result)


def parse_uri(uri, **defaults):
    """ uri 解析 """
    result = urllib.parse.urlparse(uri)
    return {
        "scheme": result.scheme,
        "username": decode_result(result.username) or defaults.get("username"),
        "password": decode_result(result.password) or defaults.get("password"),
        "netloc": result.netloc,
        "hostname": result.hostname or defaults.get("hostname"),
        "port": result.port or defaults.get("port"),
        "path": result.path,
        "query": result.query,
        "queries": urllib.parse.parse_qs(result.query, keep_blank_values=True),
        "params": result.params,
        "fragment": result.fragment,
    }


def merge_uri(parsed, **kwargs):
    """ uri 替换 """
    return urllib.parse.urlunparse(urllib.parse.ParseResult(
        scheme=kwargs.get("scheme", parsed["scheme"]),
        netloc=kwargs.get("netloc", parsed["netloc"]),
        path=kwargs.get("path", parsed["path"]),
        query=kwargs.get("query", parsed["query"]),
        params=kwargs.get("params", parsed["params"]),
        fragment=kwargs.get("fragment", parsed["fragment"]),
    ))


def update_django_db(databases, alias, uri, **default_db_values):
    """ django settings DATABASES """
    if not uri:
        return
    parsed = parse_uri(uri, **default_db_values)
    if parsed["scheme"] == "mysql":
        databases[alias] = _parse_mysql(parsed, **default_db_values)
    else:
        databases[alias] = _parse_sqlite(parsed)


def _parse_mysql(parsed, **default_db_values):
    return {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': parsed['hostname'],
        'PORT': parsed['port'],
        'USER': parsed['username'],
        'PASSWORD': parsed['password'],
        'NAME': parsed['path'].split('/')[1],
        'OPTIONS': {
            'charset': parsed['queries'].get('charset', ['utf8'])[0],
            'sql_mode': default_db_values['sql_mode'],
        },
        'TEST': {
            'charset': parsed['queries'].get('charset', ['utf8'])[0],
            'sql_mode': default_db_values['sql_mode'],
        },
    }


def _parse_sqlite(parsed):
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': parsed["path"],
    }



def parse_alias_conf(conf):
    """ Multi conf
        - "default"
        - "[alias]default"
        - "default [a]v"
        - "[a]v [b]w"
    """
    for row in conf.split():
        if row.startswith('['):
            alias, _, uri = row[1:].partition(']')
        else:
            alias, uri = "", row
        #
        if not alias:
            alias = "default"
        yield alias, uri


def update_django_dbs(databases, conf, **default_db_values):
    """ django settings DATABASES

    "default_uri [dbx]dbx_uri"
    """
    for alias, uri in parse_alias_conf(conf):
        update_django_db(databases, alias, uri, **default_db_values)


def _update_django_cache(caches, alias, uri):
    if not uri:
        return
    parsed = parse_uri(uri)
    if parsed["scheme"] == "memcached":
        caches[alias] = {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': parsed['netloc'],
        }
    elif parsed["scheme"] == "redis":
        loc = parsed["hostname"]
        if parsed["port"]:
            loc += ":{}".format(parsed["port"])
        caches[alias] = {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': [loc],
            'OPTIONS': {
                'DB': int(parsed['path'].strip('/') or 1),
            },
        }
    elif parsed["scheme"] == "locmem":
        caches[alias] = {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }


def update_django_caches(caches, conf):
    """ django settings CACHES

    "default_uri [dbx]dbx_uri"
    """
    for alias, uri in parse_alias_conf(conf):
        _update_django_cache(caches, alias, uri)
    return caches
