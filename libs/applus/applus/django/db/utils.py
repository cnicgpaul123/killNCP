# -*- coding: utf-8 -*-
""" Django Database Router """
# pylint: disable=unused-argument,invalid-name,no-self-use
from django.conf import settings
from django.db.models import Model
from django.utils.functional import cached_property


class ConfigurableDatabaseRouter:
    """ 根据配置决定数据库路由分配 """

    def _db_for_app(self, app):
        """ 获取 DB Alias
        Args：
            app: Instance／Model／Meta／app_label
        Return：
            DBalias or None
        """
        # 得出app_label: Instance -> Model -> Meta -> app_label
        if isinstance(app, Model):
            app = app.__class__
        # pylint: disable=protected-access
        if hasattr(app, '_meta'):
            app = app._meta
        if hasattr(app, 'app_label'):
            app = app.app_label
        # 是否缓存
        return self.mapping.get(app, 'default')

    @cached_property
    def mapping(self):
        """ 路由表 """
        result = {}
        try:
            conf = settings.DATABASE_APPS
        except AttributeError:
            pass
        else:
            if isinstance(conf, str):
                return self.import_from_string(conf)
            for db, apps in conf.items():
                if isinstance(apps, (list, tuple)):
                    for app in apps:
                        result[app] = db
                else:
                    result[apps] = db
        return result

    @staticmethod
    def import_from_string(router):
        """ 文本配置

        dbx=app3,app4 dby=app8,app9
        """
        result = {}
        for rule in router.split():
            db, _, apps = rule.partition("=")
            for app in apps.split(","):
                result[app] = db
        return result

    @cached_property
    def never_migrates(self):
        """ 是否禁止 migrate """
        try:
            return settings.DATABASE_NEVER_MIGRATES
        except AttributeError:
            return ()

    @cached_property
    def always_migrates(self):
        """ 是否允许 migrate """
        try:
            return settings.DATABASE_ALWAYS_MIGRATES
        except AttributeError:
            return ()

    def db_for_read(self, model, **hints):
        """ 读路由
        """
        return self._db_for_app(model)

    def db_for_write(self, model, **hints):
        """ 写路由
        """
        return self._db_for_app(model)

    def allow_relation(self, obj1, obj2, **hints):
        """ 是否允许建立关联（跨库无法实现）
        """
        return self._db_for_app(obj1) == self._db_for_app(obj2)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ 是否允许自动处理数据库变更（makemigrations、migrate）
        """
        if db in self.never_migrates:
            return False
        if db in self.always_migrates:
            return True
        # 其他数据库：只处理跟本APP相关的数据
        return self._db_for_app(app_label) == db
