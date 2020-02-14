""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.staticfiles.urls')),
    # *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    path('views/auth/', include('rest_framework.urls')),
    path('views/', include('libtest.urls')),
    path('api/admin/', include('drf_auth.admin.urls')),
    path('api/', include('drf_auth.api.urls')),
    # path('views/qrcode/', include('general_qrcode.urls')),
    #
    # path('api/', include('libtest.exceptions.urls')),
    # path('api/', include('libtest.biz.urls')),
    #
    # path('api/admin/', include('libtest.admin.urls')),
]
