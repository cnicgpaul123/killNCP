# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,protected-access,too-few-public-methods
import unittest
from rest_framework.permissions import IsAdminUser
from applus.rest_framework import permissions


__all__ = ['TestPermission']


class User:

    def __init__(self, is_superuser, is_staff):
        self.is_superuser = is_superuser
        self.is_staff = is_staff


class Request:

    def __init__(self, user):
        self.user = user


class IsSuperUser(IsAdminUser):

    def has_permission(self, request, view):
        return request.user.is_superuser


class NormalToAdmin(IsAdminUser):

    def has_object_permission(self, request, view, obj):
        return obj.is_staff


class NormalToSuper(IsAdminUser):

    def has_object_permission(self, request, view, obj):
        return obj.is_superuser


class TestPermission(unittest.TestCase):

    # pylint: disable=invalid-name,too-many-arguments
    def _try(self, perm, request_user, obj, hp, hop):
        instance = perm()
        request = Request(request_user)
        self.assertEqual(hp, instance.has_permission(request, None))
        self.assertEqual(hop, instance.has_object_permission(request, None, obj))

    def test_normal_permissions(self):
        # pylint: disable=invalid-name,invalid-unary-operand-type
        su = User(is_superuser=True, is_staff=True)
        au = User(is_superuser=False, is_staff=True)
        nu = User(is_superuser=False, is_staff=False)
        ANot2A = IsAdminUser & ~NormalToAdmin
        SNot2S = IsSuperUser & ~NormalToSuper
        OR = ANot2A | SNot2S
        ########################################################
        # <T, T> & <not T, not T/T/F>
        self._try(ANot2A, su, su, False, False) # 符合
        self._try(ANot2A, su, au, False, False) # 符合
        self._try(ANot2A, su, nu, False, True) # 不符合 <True, True>
        # <T, T> & <not T, not T/F/F>
        self._try(SNot2S, su, su, False, False) # 符合
        self._try(SNot2S, su, au, False, True) # 符合
        self._try(SNot2S, su, nu, False, True) # 不符合 <True, True>
        #
        self._try(OR, su, su, False, False) # 不符合 <True, False>
        self._try(OR, su, au, False, True) # 不符合 <True, True>
        self._try(OR, su, nu, False, True) # 不符合 <True, True>
        ########################################################
        # <T, T> & <not T, not T/T/F>
        self._try(ANot2A, au, su, False, False) # 符合
        self._try(ANot2A, au, au, False, False) # 符合
        self._try(ANot2A, au, nu, False, True) # 不符合 <True, True>
        # <F, T> & <not F, not T/F/F>
        self._try(SNot2S, au, su, False, False) # 符合
        self._try(SNot2S, au, au, False, True) # 不符合 <False, False>
        self._try(SNot2S, au, nu, False, True) # 不符合 <False, False>
        #
        self._try(OR, au, su, False, False) # 不符合 <True, False>
        self._try(OR, au, au, False, True) # 不符合 <True, True>
        self._try(OR, au, nu, False, True) # 不符合 <True, True>
        ########################################################
        # <F, T> & <not F, not T/T/F>
        self._try(ANot2A, nu, su, False, False) # 符合
        self._try(ANot2A, nu, au, False, False) # 符合
        self._try(ANot2A, nu, nu, False, True) # 不符合 <False, False>
        # <F, T> & <not F, not T/F/F>
        self._try(SNot2S, nu, su, False, False) # 符合
        self._try(SNot2S, nu, au, False, True) # 不符合 <False, False>
        self._try(SNot2S, nu, nu, False, True) # 不符合 <False, False>
        #
        self._try(OR, nu, su, False, False) # 符合
        self._try(OR, nu, au, False, True) # 不符合 <False, False>
        self._try(OR, nu, nu, False, True) # 不符合 <False, False>
        ########################################################

    def test_extend_permissions(self):
        # pylint: disable=invalid-name,invalid-unary-operand-type
        su = User(is_superuser=True, is_staff=True)
        au = User(is_superuser=False, is_staff=True)
        nu = User(is_superuser=False, is_staff=False)
        ANot2A = permissions.FromAdmin & ~permissions.ToAdmin
        SNot2S = permissions.FromSuper & ~permissions.ToSuper
        OR = ANot2A | SNot2S
        PERM = IsAdminUser & OR
        ########################################################
        # <T, T> & <T, not T/T/F>
        self._try(ANot2A, su, su, True, False) # 符合
        self._try(ANot2A, su, au, True, False) # 符合
        self._try(ANot2A, su, nu, True, True) # 符合
        # <T, T> & <T, not T/F/F>
        self._try(SNot2S, su, su, True, False) # 符合
        self._try(SNot2S, su, au, True, True) # 符合
        self._try(SNot2S, su, nu, True, True) # 符合
        #
        self._try(OR, su, su, True, False) # 符合
        self._try(OR, su, au, True, True) # 符合
        self._try(OR, su, nu, True, True) # 符合
        #
        self._try(PERM, su, su, True, False) # 符合
        self._try(PERM, su, au, True, True) # 符合
        self._try(PERM, su, nu, True, True) # 符合
        ########################################################
        # <T, T> & <T, not T/T/F>
        self._try(ANot2A, au, su, True, False) # 符合
        self._try(ANot2A, au, au, True, False) # 符合
        self._try(ANot2A, au, nu, True, True) # 符合
        # <T, F> & <T, not T/F/F>
        self._try(SNot2S, au, su, True, False) # 符合
        self._try(SNot2S, au, au, True, False) # 符合
        self._try(SNot2S, au, nu, True, False) # 符合
        #
        self._try(OR, au, su, True, False) # 符合
        self._try(OR, au, au, True, False) # 符合
        self._try(OR, au, nu, True, True) # 符合
        #
        self._try(PERM, au, su, True, False) # 符合
        self._try(PERM, au, au, True, False) # 符合
        self._try(PERM, au, nu, True, True) # 符合
        ########################################################
        # <T, F> & <T, not T/T/F>
        self._try(ANot2A, nu, su, True, False) # 符合
        self._try(ANot2A, nu, au, True, False) # 符合
        self._try(ANot2A, nu, nu, True, False) # 符合
        # <T, F> & <T, not T/F/F>
        self._try(SNot2S, nu, su, True, False) # 符合
        self._try(SNot2S, nu, au, True, False) # 符合
        self._try(SNot2S, nu, nu, True, False) # 符合
        #
        self._try(OR, nu, su, True, False) # 符合
        self._try(OR, nu, au, True, False) # 符合
        self._try(OR, nu, nu, True, False) # 符合
        #
        self._try(PERM, nu, su, False, False) # 符合
        self._try(PERM, nu, au, False, False) # 符合
        self._try(PERM, nu, nu, False, False) # 符合
        ########################################################
