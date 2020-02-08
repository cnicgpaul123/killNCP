# -*- coding: utf-8 -*-
""" 改进 rest_framework 的错误处理
原来的错误响应内容有多种可能，数据结构各不相同，对文档编写/前端对接造成较大困扰。

[
    {
        "field": null,
        "code": "parse_error",
        "message": "错误的请求。"
    }
]
@router.register_decorator("error/400", base_name="rest-err-400-parse")
class ParseErrorViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.ParseError()


[
    {
        "field": null,
        "code": "not_authenticated",
        "message": "身份认证信息未提供。"
    }
]
# OR
{
    "message": "Authenticated"
}
@router.register_decorator("error/401/not", base_name="rest-err-401-not")
class NotAuthenticatedViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        return response.Response({"message": "Authenticated"})


[
    {
        "field": null,
        "code": "permission_denied",
        "message": "您没有执行该操作的权限。"
    }
]
# OR
[
    {
        "field": null,
        "code": "not_authenticated",
        "message": "身份认证信息未提供。"
    }
]
@router.register_decorator("error/401/fail", base_name="rest-err-401-fail")
class AuthenticationFailedViewSet(viewsets.ViewSet):

    permission_classes = [NeverPermission]
    def list(self, request, *args, **kwargs):
        return response.Response({"message": "Something's wrong if you can see this message."})


[
    {
        "field": null,
        "code": "permission_denied",
        "message": "您没有执行该操作的权限。"
    }
]
@router.register_decorator("error/403/django", base_name="rest-err-403-django")
class DjangoPermissionDeniedViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise PermissionDenied


[
    {
        "field": null,
        "code": "permission_denied",
        "message": "您没有执行该操作的权限。"
    }
]
@router.register_decorator("error/403", base_name="rest-err-403")
class PermissionDeniedViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.PermissionDenied()


[
    {
        "field": null,
        "code": "not_found",
        "message": "未找到。"
    }
]
@router.register_decorator("error/404/django", base_name="rest-err-404-django")
class DjangoNotFoundViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise Http404


[
    {
        "field": null,
        "code": "not_found",
        "message": "未找到。"
    }
]
@router.register_decorator("error/404", base_name="rest-err-404")
class NotFoundViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.NotFound()


[
    {
        "field": null,
        "code": "method_not_allowed",
        "message": "方法 “GET” 不被允许。"
    }
]
@router.register_decorator("error/405", base_name="rest-err-405")
class NotAllowedViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        return response.Response({"message": "nop"})


[
    {
        "field": null,
        "code": "not_acceptable",
        "message": "无法满足Accept HTTP头的请求。"
    }
]
@router.register_decorator("error/406", base_name="rest-err-406")
class NotAcceptableViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable()


[
    {
        "field": null,
        "code": "unsupported_media_type",
        "message": "不支持请求中的媒体类型 “application/unknown”。"
    }
]
@router.register_decorator("error/415", base_name="rest-err-415")
class UnsupportedMediaTypeViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.UnsupportedMediaType("application/unknown")


[
    {
        "field": null,
        "code": "throttled",
        "message": "请求超过了限速。"
    }
]
@router.register_decorator("error/429", base_name="rest-err-429")
class ThrottledViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        raise exceptions.Throttled()

"""
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.settings import api_settings
from rest_framework import exceptions
from rest_framework import views
from rest_framework.response import Response


def _convert_exception(exc):
    if isinstance(exc, Http404):
        return exceptions.NotFound()
    if isinstance(exc, PermissionDenied):
        return exceptions.PermissionDenied()
    return exc


def _make_response_data(exc):
    # if not isinstance(exc, exceptions.ValidationError):
    #     return _get_full_details(exc.detail, None, True)
    return _get_full_details([], exc.detail, None, True)


def _process_field_name(field_name, root, field):
    if not root:
        return field
    if field_name == api_settings.NON_FIELD_ERRORS_KEY:
        return None
    return field_name


def _get_full_details(results, detail, field, root):
    if isinstance(detail, list):
        for item in detail:
            _get_full_details(results, item, field, False)
    elif isinstance(detail, dict):
        for field_name, field_detail in detail.items():
            _get_full_details(results,
                              field_detail,
                              _process_field_name(field_name, root, field),
                              False)
    else:
        results.append({
            "field": field,
            "code": detail.code,
            "message": detail,
        })
    return results


# pylint: disable=unused-argument
def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    exc = _convert_exception(exc)
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        # Original implementation:
        #
        # if isinstance(exc.detail, (list, dict)):
        #     data = exc.detail
        # else:
        #     data = {'detail': exc.detail}
        #
        data = _make_response_data(exc)

        views.set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
