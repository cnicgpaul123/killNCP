# -*- coding: utf-8 -*-
""" 令牌管理
"""
from django.db import models


class AuthTokenManager(models.Manager):
    """ 令牌管理(rest_framework.authtoken.models) """

    def fetch(self, raise_exception=False, **kwargs):
        """ 获取令牌，不存在自动生成 """
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            if raise_exception:
                raise
            return self.create(**kwargs)

    def refresh(self, **kwargs):
        """ 刷新令牌 """
        self.filter(**kwargs).delete()
        return self.create(**kwargs)
