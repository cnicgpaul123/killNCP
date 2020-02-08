# -*- coding: utf-8 -*-
""" Model/Manager/Queryset utils and lazy """
from functools import partial
from django.conf import settings
from django.apps import apps
from django.utils import functional
from django.utils import module_loading


def get_model(alias):
    """ Model
    """
    if not alias:
        alias = settings.AUTH_USER_MODEL
    return apps.get_model(alias)


def get_dao(alias, dao_class_or_namespace=None):
    """ Manager
    """
    model = get_model(alias)
    if not dao_class_or_namespace:
        return model.objects

    if isinstance(dao_class_or_namespace, str):
        dao_class = module_loading.import_string(dao_class_or_namespace)
    else:
        dao_class = dao_class_or_namespace
    dao = dao_class()
    dao.model = model
    return dao


def get_queryset(alias):
    """ Queryset
    """
    return get_dao(alias).all()


def get_lazy_model(alias):
    """ Model(lazy)
    """
    return functional.SimpleLazyObject(partial(get_model, alias))


def get_lazy_dao(alias, dao_class_or_namespace=None):
    """ Manager(lazy)
    """
    return functional.SimpleLazyObject(partial(
        get_dao, alias, dao_class_or_namespace=dao_class_or_namespace))


def get_lazy_queryset(alias):
    """ Queryset(lazy)
    """
    return functional.SimpleLazyObject(partial(get_queryset, alias))


def cached_property_dao(alias=None, dao_class_or_namespace=None):
    """ 类属性(cached_property)，可解决 import 依赖问题

    class XXX:

        token_dao = dao.cached_property_dao("authtoken.token")

    """
    # pylint: disable=unused-argument
    def _func(self):
        return get_lazy_dao(alias, dao_class_or_namespace)
    return functional.cached_property(_func)
