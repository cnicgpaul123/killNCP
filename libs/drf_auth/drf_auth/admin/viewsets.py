# -*- coding: utf-8 -*-
""" 管理员 API """
# pylint: disable=too-many-ancestors,unused-argument,no-self-use,invalid-name
# pylint: disable=invalid-unary-operand-type
from rest_framework import viewsets
from rest_framework.response import Response
from applus.rest_framework import routers
from applus.rest_framework import permissions
from .. import serializers


admin_router = routers.PerformRouter()

# 角色限定：运营人员
# 对象限定：普通用户、超级管理员对非超管
Admin2userOrSuper2staff = permissions.IsAdminUser & (
    ~permissions.ToAdmin |
    (permissions.FromSuper & ~permissions.ToSuper))


@admin_router.register_decorator('users', base_name="admin-user", include="LCR")
class UserViewSet(admin_router.perform_mixin, viewsets.ModelViewSet):
    """ 用户管理

        - 用户列表(管理员)
        - 用户详情(管理员)
        - 创建帐号(超级管理员)
        - 修改密码(超级管理员可以修改所有、普通管理员仅可修改自身)
    """

    permission_classes = [permissions.IsAdminUser]
    # queryset = serializers.user_dao
    lookup_field = 'username'
    lookup_value_regex = '[^/]+' # 允许 email 形式 “master@qq.com”
    serializer_class = serializers.UserForAdminSerializer
    filter_fields = ['is_superuser', 'is_staff', 'is_active']
    search_fields = ['username']

    extra_permission_classes = {
        #
        # 角色限定：超级管理员
        'create': [permissions.IsSuperUser],
        #
        # 角色限定：超级管理员
        'token': [permissions.IsSuperUser],
        #
        # 角色限定：运营人员
        # 对象限定：普通用户、超级管理员对非超管
        'password': [Admin2userOrSuper2staff],
        #
        # 角色限定：运营人员
        # 对象限定：普通用户、超级管理员对非超管
        'active': [Admin2userOrSuper2staff],
    }
    extra_serializer_classes = {
        'create': serializers.CreateStaffSerializer,
        'password': serializers.PasswordResetSerializer,
        'active': serializers.IsActiveSerializer,
    }

    def get_queryset(self):
        return serializers.user_dao.order_by('id')

    @admin_router.action(['get'], detail=True)
    def token(self, *args, **kwargs):
        """ 获取令牌 """
        instance = self.get_object()
        token = serializers.token_dao.fetch(user_id=instance.id)
        serializer = serializers.TokenSerializer(instance=token)
        return Response(serializer.data)

    @admin_router.action(['put'], detail=True)
    @admin_router.perform_decorator()
    def password(self, *args, **kwargs):
        """ 通过 perform_extra_action 自动调用 perform_${ACTION} """

    # pylint: disable=protected-access
    def perform_password(self, serializer):
        """ 更新密码，并调整响应内容 """
        serializer.save()
        serializer._data = {}

    @admin_router.action(['put'], detail=True)
    @admin_router.perform_decorator()
    def active(self, *args, **kwargs):
        """ 通过 perform_extra_action 自动调用 perform_${ACTION} """

    # pylint: disable=protected-access
    def perform_active(self, serializer):
        """ 更新激活状态 """
        serializer.save()
