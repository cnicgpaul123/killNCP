# -*- coding: utf-8 -*-
""" 封装 path, re_path """
from django.urls import path, re_path


class BaseRouter:
    """ 封装 path, re_path

    urlpatterns = [
        path('html/hello/', views.hello),
        path('html/say/<str:word>/', views.say),
        re_path(r'^html/articles/(?P<year>[0-9]{4})/$', views.year_archive),
        re_path(r'^html/articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    ]
    ==>
    urlpatterns = views.router.urls
    @router.register_path('html/hello/')
    @router.register_path('html/say/<str:word>/')
    @router.register_re(r'^html/articles/(?P<year>[0-9]{4})/$')
    @router.register_re(r'^html/articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$')
    """

    PATTERN_PATH = 'path'
    PATTERN_RE = 're'

    def __init__(self):
        self.registry = []

    def _register(self, route, re_mode, *args, **kwargs):
        def decorator(view):
            self.registry.append((route, re_mode, view, args, kwargs))
            return view
        return decorator

    def register_path(self, route, *args, **kwargs):
        """ for path(...) """
        return self._register(route, self.PATTERN_PATH, *args, **kwargs)

    def register_re(self, route, *args, **kwargs):
        """ for re_path(...) """
        return self._register(route, self.PATTERN_RE, *args, **kwargs)

    # pylint: disable=missing-docstring,attribute-defined-outside-init
    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls

    def get_urls(self):
        """ Use the registered paths to generate a list of URL patterns. """
        ret = []
        for (route, re_mode, view, args, kwargs) in self.registry:
            if re_mode == self.PATTERN_RE:
                ret.append(re_path(route, view, *args, **kwargs))
            else:
                ret.append(path(route, view, *args, **kwargs))
        return ret
