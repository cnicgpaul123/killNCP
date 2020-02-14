# -*- coding: utf-8 -*-
""" 权限 """
# pylint: disable=unused-import,no-self-use,unused-argument,too-few-public-methods
from operator import eq
from django.utils import six
from rest_framework.permissions import (
    BasePermission, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)


class IsSuperUser(BasePermission):
    """ 角色限定：超级管理员 """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


def from_attr(attr, expected, base=BasePermission, operator=eq):
    """ 利用对象的属性生成 permission 类
    """
    # pylint: disable=too-few-public-methods,unused-argument,no-self-use
    class AttrPermission(base):
        """ 根据属性判断权限 """

        def has_object_permission(self, request, view, obj):
            """ 算子(属性、期望值) """
            return operator(getattr(obj, attr), expected)

    return AttrPermission


def from_method(method, *args, base=BasePermission, **kwargs):
    """ 利用对象类方法生成 permission 类
    """
    # pylint: disable=too-few-public-methods,unused-argument,no-self-use
    class MethodPermission(base):
        """ 使用指定方法判断权限 """

        def has_object_permission(self, request, view, obj):
            """ 根据执行结果判定 """
            return method(obj, *args, **kwargs)

    return MethodPermission


#################################
# BaseObjectPermissionMetaclass #
#################################

class ObjectOperationHolderMixin:
    """ 操作符辅助类 """

    def __and__(self, other):
        return ObjectOperandHolder(OAND, self, other)

    def __or__(self, other):
        return ObjectOperandHolder(OOR, self, other)

    def __rand__(self, other):
        return ObjectOperandHolder(OAND, other, self)

    def __ror__(self, other):
        return ObjectOperandHolder(OOR, other, self)

    def __invert__(self):
        return SingleObjectOperandHolder(ONOT, self)


class SingleObjectOperandHolder(ObjectOperationHolderMixin):
    """ 单目操作辅助类 """
    def __init__(self, operator_class, op1_class):
        self.operator_class = operator_class
        self.op1_class = op1_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        return self.operator_class(op1)


class ObjectOperandHolder(ObjectOperationHolderMixin):
    """ 二元操作辅助类 """
    def __init__(self, operator_class, op1_class, op2_class):
        self.operator_class = operator_class
        self.op1_class = op1_class
        self.op2_class = op2_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        op2 = self.op2_class(*args, **kwargs)
        return self.operator_class(op1, op2)


class OAND:
    """ 两个类“与”结合 """
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """ 原方法结果“与”计算 """
        return (
            self.op1.has_object_permission(request, view, obj) and
            self.op2.has_object_permission(request, view, obj)
        )


class OOR:
    """ 两个类“或”结合 """
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """ 原方法结果“或”计算 """
        return (
            self.op1.has_object_permission(request, view, obj) or
            self.op2.has_object_permission(request, view, obj)
        )


class ONOT:
    """ 原始类“取反” """
    def __init__(self, op1):
        self.op1 = op1

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """ 原方法结果“反”计算 """
        return not self.op1.has_object_permission(request, view, obj)


class BaseObjectPermissionMetaclass(ObjectOperationHolderMixin, type):
    """
    BasePermissionMetaclass 的新特性( &,|,~ )有些问题：
    如果要实现“允许管理员对非管理员，或超管对非超管”
    可以参考 test/test_permission.py 的测试用例和结果

    参考 BasePermissionMetaclass，实现了 BaseObjectPermissionMetaclass

    实践中继承 BasePermission 时推荐：
    - 按需实现 has_permission(...)
    - has_object_permission(...) 默认返回 True
    - Permission 不要合并多次(and/or 结果不符合预期)

    实践中继承 BaseObjectPermission 时推荐：
    - has_permission(...) 默认返回 True
    - 按需实现 has_object_permission(...)

    首先组合 BaseObjectPermission:
        X & Y
        X | Y
        ~Z

    最后组合成 Permission:
        SomePermissionClass & ( Combined Object Permission Class )

    “允许管理员对非管理员，或超管对非超管”实现示例：
    IsAdminUser & ( (FromSuper & ~ToSuper) | (FromAdmin & ~ToAdmin) )
    参考 test/test_permission.py 的测试用例和结果
    """


@six.add_metaclass(BaseObjectPermissionMetaclass)
class BaseObjectPermission:
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return False


###########################
# user object permissions #
###########################

class FromAdmin(BaseObjectPermission):
    """ 角色限定：管理员 """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class FromSuper(BaseObjectPermission):
    """ 角色限定：超级管理员 """

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class ToAdmin(BaseObjectPermission):
    """ 对象限定：管理员 """

    def has_object_permission(self, request, view, obj):
        return obj.is_staff


class ToSuper(BaseObjectPermission):
    """ 对象限定：超级管理员 """

    def has_object_permission(self, request, view, obj):
        return obj.is_superuser


class ToSelf(BaseObjectPermission):
    """ 对象限定：自己 """

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
