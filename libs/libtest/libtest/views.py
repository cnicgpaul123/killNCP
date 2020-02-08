# pylint: disable=missing-docstring,invalid-name,unused-argument
from django.http import HttpResponse
from applus.django import routers


router = routers.BaseRouter()


# path('html/hello/', views.hello)
@router.register_path('html/hello/')
def hello(request):
    return HttpResponse("hello, world")


# path('html/say/<str:word>/', views.say)
@router.register_path('html/say/<str:word>/')
def say(request, word):
    return HttpResponse("say: `{}`".format(word))


# re_path(r'^html/articles/(?P<year>[0-9]{4})/$', views.year_archive)
@router.register_re(r'^html/articles/(?P<year>[0-9]{4})/$')
def year_archive(request, year):
    return HttpResponse("Archive(year={})".format(year))


# re_path(r'^html/articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive)
@router.register_re(r'^html/articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$')
def month_archive(request, year, month):
    return HttpResponse("Archive(year={}, month={})".format(year, month))

@router.register_re(r'^html/articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$')
def day_archive(resuest, year, month, day):
    return HttpResponse("Archive(year={}, month={}, day={}".format(year, month, day))