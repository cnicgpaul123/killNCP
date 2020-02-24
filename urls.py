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
from rest_framework.routers import DefaultRouter


from personinfo_app import views
router = DefaultRouter()
router.register(r'api/personinfo', views.PersonInfoViewSet, base_name="personinfos")


urlpatterns = [
    path('', include('django.contrib.staticfiles.urls')),

    path('views/auth/', include('rest_framework.urls')),
    path('api/admin/', include('drf_auth.admin.urls')),
    path('api/', include('drf_auth.api.urls')),
    # path('api/admin/', include('drf_auth.admin.urls')),
    # path('api/', include('drf_auth.api.urls')),
    
    # personinfo api 
    path(r'', include(router.urls)),
    path('api/exportexcel/', views.ExportExcelView.as_view(), name='export_person'),
    path('api/personinfoiscreate/', views.PersonInfoIsCreateView.as_view(), name='personinfo_is_create'),
    path('api/visitinfo/', views.VisitInfoCreateView.as_view(), name='visitinfo'),

]
