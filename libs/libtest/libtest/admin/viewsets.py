# -*- coding: utf-8 -*-
""" 管理员 API """
# pylint: disable=too-many-ancestors,unused-argument,no-self-use,invalid-name
from rest_framework import viewsets
from rest_framework import permissions
from applus.rest_framework import routers
from applus.rest_framework.permissions import IsSuperUser
from applus.django import dao
from .. import serializers


admin_router = routers.PerformRouter()


class IsSuperOrStaffSelf(permissions.IsAdminUser):
    """ 仅允许超级用户、或管理员自己 """

    def has_object_permission(self, request, view, obj):
        """ 仅允许超级用户、或管理员自己 """
        return request.user.is_superuser or request.user.id == obj.id


@admin_router.register_decorator('users', base_name="admin-user", include="LCR")
class UserViewSet(admin_router.perform_mixin, viewsets.ModelViewSet):
    """ 用户管理

        - 用户列表(管理员)
        - 用户详情(管理员)
        - 创建帐号(超级管理员)
        - 修改密码(超级管理员可以修改所有、普通管理员仅可修改自身)
    """

    permission_classes = [permissions.IsAdminUser]
    queryset = dao.get_lazy_queryset(None)
    serializer_class = serializers.UserForAdminSerializer

    extra_permission_classes = {
        'create': [IsSuperUser],
        'password': [IsSuperOrStaffSelf],
    }
    extra_serializer_classes = {
        'create': serializers.CreateStaffSerializer,
        'password': serializers.PasswordResetSerializer,
    }

    @admin_router.action(['put'], detail=True)
    @admin_router.perform_decorator()
    def password(self, *args, **kwargs):
        """ 通过 perform_extra_action 自动调用 perform_${ACTION} """

    # pylint: disable=protected-access
    def perform_password(self, serializer):
        """ 更新密码，并调整响应内容 """
        serializer.save()
        serializer._data = {}
