# -*- coding: utf-8 -*-
""" 扩展 rest_framework Router 功能
"""
from inspect import getmembers
import functools
from django.core.exceptions import ImproperlyConfigured
from django.utils import functional
from rest_framework import routers
from rest_framework import decorators
from rest_framework import response


class Router(routers.DefaultRouter):
    """ register 扩展辅助

    class TestView:
        pass

    router.register(prefix, TestView, ...)

    ==>

    @router.register(prefix, ...)
    class TestView:
        pass
    """

    @classmethod
    def action(cls, *args, **kwargs):
        """ 引入 action 装饰器 """
        return decorators.action(*args, **kwargs)

    def _register(self, prefix, viewset, *args, **kwargs):
        self.register(prefix, viewset, *args, **kwargs)

    def register_decorator(self, prefix, *args, **kwargs):
        """ register 辅助装饰器 """
        def decorator(viewset):
            self._register(prefix, viewset, *args, **kwargs)
            return viewset
        return decorator


class FilterRouter(Router):
    """ register 可限定/排除指定 actions(适用于 ModelViewSet)
    i.e.
        (..., include='LRP')
        OR
        (..., exclude='list retrieve partial_update')
        OR
        (..., include=('list', 'retrieve', 'partial_update'))
    """

    def __init__(self, *args, **kwargs):
        super(FilterRouter, self).__init__(*args, **kwargs)
        self.exclude_method_map = {}
        self.cached_methods = {}

    def _register(self, prefix, viewset, *args, **kwargs):
        include_actions = kwargs.pop('include', None)
        exclude_actions = kwargs.pop('exclude', None)
        self._set_bind_actions(viewset, include_actions, exclude_actions)
        super(FilterRouter, self)._register(prefix, viewset, *args, **kwargs)

    def _set_bind_actions(self, viewset, include_actions, exclude_actions):
        known_methods = [
            cls_method
            for cls_method, http_method in self._support_mapping.items()
            if hasattr(viewset, cls_method)
        ]
        exclude_methods = []
        if include_actions is not None:
            include_methods = self._get_methods(include_actions)
            for cls_method in known_methods:
                if cls_method not in include_methods:
                    exclude_methods.append(cls_method)
        if exclude_actions is not None:
            for cls_method in self._get_methods(exclude_actions):
                if cls_method in known_methods:
                    exclude_methods.append(cls_method)
        if exclude_methods:
            self.exclude_method_map[viewset] = exclude_methods

    @functional.cached_property
    def _support_mapping(self):
        results = {}
        for route in self.routes:
            if not hasattr(route, 'mapping'):
                continue
            for http_method, cls_method in route.mapping.items():
                results[cls_method] = http_method
        return results

    @functional.cached_property
    def _support_mapping_keys(self):
        return sorted(list(self._support_mapping.keys()))

    def _get_methods(self, actions):
        origin = actions
        if origin in self.cached_methods:
            return self.cached_methods[origin]
        if isinstance(actions, str):
            actions = self._convert_actions(actions)
        methods = []
        for action in actions:
            for cls_method in self._support_mapping_keys:
                if cls_method.startswith(action.lower()):
                    methods.append(cls_method)
                    break
        self.cached_methods[origin] = methods
        return methods

    @classmethod
    def _convert_actions(cls, actions):
        actions = actions.lower()
        for delim in '|,;:':
            if delim in actions:
                return actions.split(delim)
        if ' ' in actions:
            return actions.split()
        return list(actions)

    def get_method_map(self, viewset, method_map):
        """
        Given a viewset, and a mapping of http methods to actions,
        return a new mapping which only includes any mappings that
        are actually implemented by the viewset.
        """
        filtered_map = method_map
        if viewset in self.exclude_method_map:
            exclude_methods = self.exclude_method_map[viewset]
            filtered_map = {
                http_method: cls_method
                for http_method, cls_method in method_map.items()
                if cls_method not in exclude_methods
            }
        return super(FilterRouter, self).get_method_map(viewset, filtered_map)


def _is_verb_action(attr):
    return hasattr(attr, 'verb_method')


def _get_verb_actions(viewset):
    return [
        method
        for _, method in getmembers(viewset, _is_verb_action)
    ]


class VerbRouter(FilterRouter):
    """ 提供非 detail 语义的 router 方式
    根据使用场景合理使用 route：
        1. prefix 没有后续 url，使用 L/C;
        2. prefix 后续 url 有 lookup/detail/instance 语义，使用 R/U/P/D 或者 action；
        3. prefix 后续 url 是常量(也就没有 lookup/detail/instance 语义)，使用 verb；
    """

    @classmethod
    def verb(cls, method=None, url_path=None, url_name=None, **kwargs):
        """ 装饰器 """
        def decorator(func):
            func.verb_method = (method or "get").lower()
            func.url_path = url_path if url_path else func.__name__
            if not url_name:
                func.url_name = func.__name__.replace('_', '-')
            else:
                func.url_name = url_name
            func.kwargs = kwargs
            return func
        return decorator

    # pylint: disable=no-self-use
    def _get_verb_route(self, action):
        initkwargs = action.kwargs.copy()
        url_path = routers.escape_curly_brackets(action.url_path)
        url = r'^{prefix}/{url_path}{trailing_slash}$'
        name = '{basename}-{url_name}'
        return routers.Route(
            url=url.replace('{url_path}', url_path),
            mapping={action.verb_method: action.__name__},
            name=name.replace('{url_name}', action.url_name),
            detail=None,
            initkwargs=initkwargs)

    def get_routes(self, viewset):
        """ append verb routers. """
        defaults = super(VerbRouter, self).get_routes(viewset)
        #
        verb_actions = _get_verb_actions(viewset)
        # checking action names against the known actions list
        not_allowed = [
            action.__name__ for action in verb_actions
            if action.__name__ in self._support_mapping_keys
        ]
        if not_allowed:
            msg = ('Cannot use the @verb decorator on the following '
                   'methods, as they are existing routes: %s')
            raise ImproperlyConfigured(msg % ', '.join(not_allowed))
        #
        verb_routes = [
            self._get_verb_route(action)
            for action in verb_actions
        ]
        # 必须把扩展 Route 放置在默认之前(否则，detail/lookup Pattern 会优先使用)
        return verb_routes + defaults


class PerformViewSetMixin:
    """ 扩展 permissions/serializer """

    extra_permission_classes = None
    extra_serializer_classes = None

    @staticmethod
    def _get_value_by_action(action, container, default):
        if not container:
            return default
        for key, value in container.items():
            if isinstance(key, str):
                if key == action:
                    return value
            elif action in key:
                return value
        return default

    def get_permissions(self):
        """ 权限扩展 """
        results = super(PerformViewSetMixin, self).get_permissions()
        extra = self._get_value_by_action(
            self.action,
            self.extra_permission_classes,
            ())
        for permission_class in extra:
            results.append(permission_class())
        return results

    def get_serializer_class(self):
        """ 序列化扩展 """
        spec = self._get_value_by_action(
            self.action,
            self.extra_serializer_classes,
            None)
        if spec:
            return spec
        return super(PerformViewSetMixin, self).get_serializer_class()

    # pylint: disable=unused-argument,protected-access
    def perform_extra_action(self, request, *args, **kwargs):
        """ verb 对应的通用处理 """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        method_name = 'perform_%s' % self.action
        method = getattr(self, method_name)
        method(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class PerformRouter(VerbRouter):
    """ 自定义 perform 处理

    class UserViewSet(router.perform_mixin, viewsets.ModelViewSet):

        @router.action(['put'], detail=True)
        @router.perform_decorator()
        def password(self, *args, **kwargs):
            # 空内容，通过 perform_extra_action 自动调用 perform_${ACTION}
            pass

        def perform_password(self, serializer):
            ...

    """

    perform_mixin = PerformViewSetMixin

    @classmethod
    def perform_decorator(cls):
        """ perform_extra_action 装饰器 """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                return self.perform_extra_action(*args, **kwargs)
            return wrapper
        return decorator
