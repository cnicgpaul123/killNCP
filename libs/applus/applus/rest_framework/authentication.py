# -*- coding: utf-8 -*-
""" Provides various authentication policies. """
from django.conf import settings
from django.utils import functional
from rest_framework import authentication


class MultiKeywordsTokenAuthentication(authentication.TokenAuthentication):
    """
    Multi keywords token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "XXX ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    OR
        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    @functional.cached_property
    # pylint: disable=no-self-use
    def keywords(self):
        """ 允许多关键字 """
        return getattr(settings, 'AUTH_TOKEN_KEYWORDS', ['Bearer', 'Token'])

    def _match_keywords(self, given):
        # Base from rest_framework.authentication.TokenAuthentication.authenticate(...)
        #
        # if not auth or auth[0].lower() != self.keyword.lower().encode():
        #     ...
        for item in self.keywords:
            if item.lower().encode() == given.lower():
                self.keyword = item
                break

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if auth:
            self._match_keywords(auth[0])
        return super(MultiKeywordsTokenAuthentication, self).authenticate(request)
