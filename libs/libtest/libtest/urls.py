# pylint: disable=missing-docstring,invalid-name
from . import views


# urlpatterns = [
#     path('html/hello/', views.hello),
#     path('html/say/<str:word>/', views.say),
#     re_path(r'^html/articles/(?P<year>[0-9]{4})/$', views.year_archive),
#     re_path(r'^html/articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
# ]
urlpatterns = views.router.urls
