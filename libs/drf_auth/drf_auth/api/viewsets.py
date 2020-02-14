# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,too-many-ancestors,unused-argument,no-self-use,invalid-name
from django.contrib import auth
from rest_framework import viewsets
from rest_framework import response
from rest_framework import exceptions
from rest_framework import status
from applus.rest_framework import routers
from applus.rest_framework import permissions
from .. import serializers


router = routers.PerformRouter()


@router.register_decorator("auth", base_name="api-auth", include="")
class AuthViewSet(router.perform_mixin, viewsets.ViewSet):
    """ 登入/登出/帐号 """

    permission_classes = []

    @router.verb("POST")
    def login(self, request, *args, **kwargs):
        """ 登入 """
        serializer = serializers.LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.instance or not serializer.instance.id:
            raise exceptions.AuthenticationFailed
        auth.login(request, serializer.instance)
        #
        resp = self.profile(request, *args, **kwargs)
        resp.status_code = status.HTTP_201_CREATED
        return resp

    @router.verb("delete")
    def logout(self, request, *args, **kwargs):
        """ 登出 """
        if request.user and request.user.id:
            auth.logout(request)
        return response.Response({})

    @router.verb()
    def profile(self, request, *args, **kwargs):
        """ 帐号 """
        if not request.user or not request.user.id:
            return response.Response({})
        serializer = serializers.ProfileUserSerializer(instance=request.user)
        return response.Response(serializer.data)

    @router.verb()
    def token(self, request, *args, **kwargs):
        """ 令牌 """
        if not request.user or not request.user.id:
            return response.Response({})
        instance = serializers.token_dao.fetch(user_id=request.user.id)
        serializer = serializers.TokenSerializer(instance=instance)
        return response.Response(serializer.data)

    extra_permission_classes = {
        'password': [permissions.IsAuthenticated],
        'retoken': [permissions.IsAuthenticated],
    }
    extra_serializer_classes = {
        'password': serializers.PasswordChangeSerializer,
        'retoken': serializers.TokenChangeSerializer,
    }

    def get_object(self):
        """ Returns current user """
        return self.request.user

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
        return serializer_class(*args, **kwargs)

    @router.verb('PUT')
    @router.perform_decorator()
    def password(self, *args, **kwargs):
        """ 通过 perform_extra_action 自动调用 perform_${ACTION} """

    # pylint: disable=protected-access
    def perform_password(self, serializer):
        """ 更新密码，并调整响应内容 """
        serializer.save()
        serializer._data = {}

    @router.verb('PUT')
    @router.perform_decorator()
    def retoken(self, *args, **kwargs):
        """ 通过 perform_extra_action 自动调用 perform_${ACTION} """

    def perform_retoken(self, serializer):
        serializer.save()
        another = serializers.TokenSerializer(instance=serializer.instance.token)
        setattr(serializer, '_data', another.data)
