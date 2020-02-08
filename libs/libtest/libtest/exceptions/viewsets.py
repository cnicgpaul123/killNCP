# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-argument,no-self-use,pointless-string-statement,invalid-name
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework import response
from applus.rest_framework import routers
from . import serializers


router = routers.Router()


class NeverPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return False


@router.register_decorator("error/ok", base_name="rest-err-ok")
class OkViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        return response.Response({"reason": "Welcome"})

"""
[
    {
        "field": null,
        "code": "parse_error",
        "message": "错误的请求。"
    }
]
"""
@router.register_decorator("error/400", base_name="rest-err-400-parse")
class ParseErrorViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.ParseError()

"""
[
    {
        "field": null,
        "code": "not_authenticated",
        "message": "身份认证信息未提供。"
    }
]

{
    "message": "Authenticated"
}
"""
@router.register_decorator("error/401/not", base_name="rest-err-401-not")
class NotAuthenticatedViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        return response.Response({"message": "Authenticated"})

"""
[
    {
        "field": null,
        "code": "permission_denied",
        "message": "您没有执行该操作的权限。"
    }
]

[
    {
        "field": null,
        "code": "not_authenticated",
        "message": "身份认证信息未提供。"
    }
]
"""
@router.register_decorator("error/401/fail", base_name="rest-err-401-fail")
class AuthenticationFailedViewSet(viewsets.ViewSet):

    permission_classes = [NeverPermission]
    def list(self, request, *args, **kwargs):
        return response.Response({"message": "Something's wrong if you can see this message."})

"""
[
    {
        "field": null,
        "code": "permission_denied",
        "message": "您没有执行该操作的权限。"
    }
]
"""
@router.register_decorator("error/403/django", base_name="rest-err-403-django")
class DjangoPermissionDeniedViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise PermissionDenied

"""
[
    {
        "field": null,
        "code": "permission_denied",
        "message": "您没有执行该操作的权限。"
    }
]
"""
@router.register_decorator("error/403", base_name="rest-err-403")
class PermissionDeniedViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.PermissionDenied()

"""
[
    {
        "field": null,
        "code": "not_found",
        "message": "未找到。"
    }
]
"""
@router.register_decorator("error/404/django", base_name="rest-err-404-django")
class DjangoNotFoundViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise Http404

"""
[
    {
        "field": null,
        "code": "not_found",
        "message": "未找到。"
    }
]
"""
@router.register_decorator("error/404", base_name="rest-err-404")
class NotFoundViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.NotFound()

"""
[
    {
        "field": null,
        "code": "method_not_allowed",
        "message": "方法 “GET” 不被允许。"
    }
]
"""
@router.register_decorator("error/405", base_name="rest-err-405")
class NotAllowedViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        return response.Response({"message": "nop"})

"""
[
    {
        "field": null,
        "code": "not_acceptable",
        "message": "无法满足Accept HTTP头的请求。"
    }
]
"""
@router.register_decorator("error/406", base_name="rest-err-406")
class NotAcceptableViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable()

"""
[
    {
        "field": null,
        "code": "unsupported_media_type",
        "message": "不支持请求中的媒体类型 “application/unknown”。"
    }
]
"""
@router.register_decorator("error/415", base_name="rest-err-415")
class UnsupportedMediaTypeViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.UnsupportedMediaType("application/unknown")

"""
[
    {
        "field": null,
        "code": "throttled",
        "message": "请求超过了限速。"
    }
]
"""
@router.register_decorator("error/429", base_name="rest-err-429")
class ThrottledViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.Throttled()

################################################################################

"""
[
    {
        "field": null,
        "code": "null",
        "message": "No data provided"
    }
]
"""
@router.register_decorator("error/null", base_name="rest-err-null")
class NullUserViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = serializers.ErrorUserSerializer(data=None)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)

"""
[
    {
        "field": null,
        "code": "invalid",
        "message": "无效数据。期待为字典类型，得到的是 int 。"
    }
]
"""
@router.register_decorator("error/mapping", base_name="rest-err-mapping")
class MappingUserViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = serializers.ErrorUserSerializer(data=123)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)

"""
[
    {
        "field": null,
        "code": "run_bar",
        "message": "run_validators:bar"
    },
    {
        "field": null,
        "code": "run_foo",
        "message": "run_validators:foo"
    }
]
"""
@router.register_decorator("error/validators", base_name="rest-err-validators")
class ValidatorsUserViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = serializers.ValidatorsUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)

"""
[
    {
        "field": null,
        "code": "validate",
        "message": "validate_failed"
    }
]
"""
@router.register_decorator("error/validate", base_name="rest-err-validate")
class ValidateUserViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = serializers.ValidateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)

"""
[
    {
        "field": "username",
        "code": "fail_username_1",
        "message": "fields(username): case-1"
    },
    {
        "field": "username",
        "code": "fail_username_2",
        "message": "fields(username): case-2"
    },
    {
        "field": "password",
        "code": "fail_password_a",
        "message": "fields(password): case-a"
    },
    {
        "field": "password",
        "code": "fail_password_b",
        "message": "fields(password): case-b"
    }
]
"""
@router.register_decorator("error/fields", base_name="rest-err-fields")
class FieldsUserViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = serializers.FieldsUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)
