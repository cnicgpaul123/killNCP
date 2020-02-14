# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,too-many-ancestors,unused-argument,no-self-use
from django.utils import functional
from rest_framework import viewsets
from applus.django.dao import get_dao
from applus.django.manager import ManagerCacheMixin


class ModelCacheViewSet(viewsets.ModelViewSet):
    """ 结合 ManagerCacheMixin(models.Manager) 使用

    获取结果集时优化 SQL 语句，仅获取 ID
    # SELECT `client`.`id` FROM `client` ORDER BY `client`.`create_time` DESC  LIMIT 7;

    序列化之前，结合缓存恢复数据，注意：
    - list 时 instance 是多条数据集合
    - retrieve 时 instance 才是单条数据
    """

    dao_class = ""

    @functional.cached_property
    def dao(self):
        if isinstance(self.queryset, ManagerCacheMixin):
            return self.queryset
        if isinstance(self.dao_class, str):
            return get_dao(self.dao_class)
        if isinstance(self.dao_class, (tuple, list)):
            return get_dao(*self.dao_class)
        return self.queryset

    def get_values_queryset(self, queryset):
        return queryset.values('id')

    def get_queryset(self):
        queryset = super(ModelCacheViewSet, self).get_queryset()
        return self.get_values_queryset(queryset)

    # pylint: disable=arguments-differ
    def get_serializer(self, instance=None, **kwargs):
        if not instance:
            pass
        elif isinstance(instance, dict):
            instance = self.dao.load_cache(**instance)
        elif isinstance(instance, list) and isinstance(instance[0], dict):
            instance = [
                self.dao.load_cache(**item)
                for item in instance
            ]
        return super(ModelCacheViewSet, self).get_serializer(instance, **kwargs)
