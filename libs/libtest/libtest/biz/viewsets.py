# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,too-many-ancestors,unused-argument,no-self-use,invalid-name
from django.contrib import auth
from rest_framework import viewsets
from rest_framework import response
from rest_framework import status
from applus.rest_framework import routers
from applus.django import dao
from .. import serializers


router = routers.VerbRouter()


@router.register_decorator('filter/users', base_name="api-filter-user", include='LRP')
class IncludeUserViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.BaseUserSerializer
    queryset = dao.get_lazy_queryset(None)


@router.register_decorator('verb/users', base_name="api-verb-user", include='CR')
class VerbUserViewSet(IncludeUserViewSet):

    @router.action(detail=False)
    def act(self, request, *args, **kwargs):
        return response.Response(dict(message="`action`(detail=False) decorator affected."))

    @router.action(detail=True)
    def exec(self, request, *args, **kwargs):
        return response.Response(dict(message="`action`(detail=True) decorator affected."))

    @router.verb()
    def fetch(self, request, *args, **kwargs):
        return response.Response(dict(message="`verb`(GET) decorator affected."))

    @router.verb("POST")
    def amend(self, request, *args, **kwargs):
        return response.Response(dict(message="`verb`(POST) decorator affected."))

    @router.verb("delete")
    def erase(self, request, *args, **kwargs):
        return response.Response(dict(message="`verb`(DELETE) decorator affected."))


@router.register_decorator("auth", base_name="api-auth", include="")
class AuthViewSet(viewsets.ViewSet):
    """ 登入/登出/帐号 """

    permission_classes = []

    token_dao = dao.cached_property_dao(
        "authtoken.token",
        "applus.rest_framework.authtoken.AuthTokenManager")

    @router.verb("POST")
    def login(self, request, *args, **kwargs):
        """ 登入 """
        serializer = serializers.LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth.login(request, serializer.instance)
        #
        resp = self.profile(request, *args, **kwargs)
        resp.status_code = status.HTTP_201_CREATED
        return resp

    @router.verb("delete")
    def logout(self, request, *args, **kwargs):
        """ 登出 """
        if request.user:
            auth.logout(request)
        return response.Response({})

    @router.verb()
    def profile(self, request, *args, **kwargs):
        """ 帐号 """
        if not request.user:
            return response.Response({})
        serializer = serializers.ProfileUserSerializer(instance=request.user)
        return response.Response(serializer.data)

    @router.verb()
    def token(self, request, *args, **kwargs):
        """ 令牌 """
        if not request.user:
            return response.Response({})
        instance = self.token_dao.fetch(user_id=request.user.id)
        serializer = serializers.TokenSerializer(instance=instance)
        return response.Response(serializer.data)
