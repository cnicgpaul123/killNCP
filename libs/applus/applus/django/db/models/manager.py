# -*- coding: utf-8 -*-
""" ManagerCacheMixin """
# pylint: disable=too-few-public-methods,no-self-use
from django.conf import settings
from django.core.cache import caches, cache
from django.utils import functional
from django.utils import module_loading


class ManagerCacheMixin:
    """ ManagerCacheMixin """

    SERIALIZER_CLASS = ""

    @functional.cached_property
    def serializer_class(self):
        """ Return the class to use for the serializer. """
        if isinstance(self.SERIALIZER_CLASS, str):
            return module_loading.import_string(self.SERIALIZER_CLASS)
        return self.SERIALIZER_CLASS

    @functional.cached_property
    def cache(self):
        """ 缓存池 """
        try:
            return caches[settings.DAO_CACHE_ALIAS]
        except AttributeError:
            return cache

    def get_cache_key(self, **values):
        """ 缓存 KEY """
        raise NotImplementedError

    def clear_cache(self, **values):
        """ 清除缓存 """
        self.cache.delete(self.get_cache_key(**values))

    def load_cache(self, lookup=True, **values):
        """ 从缓存加载实例 """
        cache_key = self.get_cache_key(**values)
        serialized = self.cache.get(cache_key)
        if serialized is not None:
            return self.model(**serialized)
        if not lookup:
            return None
        instance = self.get(**values)
        serialized = self.serializer_class(instance).data
        self.cache.set(cache_key, serialized)
        return instance
