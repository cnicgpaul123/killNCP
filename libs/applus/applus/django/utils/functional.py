# -*- coding: utf-8 -*-
""" django.utils.functional 扩展 """
import functools
from django.utils import functional


def reset_lazy_object(lazied):
    """ 重置 LazyObject 到未实例化的状态

    class LazyObject:

        def __init__(self):
            self._wrapped = empty
        ...
    """
    # pylint: disable=protected-access
    lazied._wrapped = functional.empty
    # !!! Don't return it.
    #
    # In [1]: import datetime
    # In [2]: from django.utils import functional
    # In [3]: n = functional.SimpleLazyObject(datetime.datetime.now)
    # In [4]: n
    # Out[4]: <SimpleLazyObject: datetime.datetime(..., 10, 39, 50, 939029)>
    # In [5]: from applus.django.functional import reset_lazy_object
    #
    # In [6]: reset_lazy_object(n)
    # Out[6]: <SimpleLazyObject: datetime.datetime(..., 10, 40, 13, 318753)>
    ##### new instantiation immediately!
    #
    # In [7]: _ = reset_lazy_object(n)
    #### just wait a few seconds!
    # In [8]: n
    # Out[8]: <SimpleLazyObject: datetime.datetime(..., 10, 40, 38, 397132)>


def make_lazy_object(func, *args, **kwargs):
    """ SimpleLazyOjbect 扩展(默认仅接受无参数的函数) """
    partial_func = functools.partial(func, *args, **kwargs)
    return functional.SimpleLazyObject(partial_func)
