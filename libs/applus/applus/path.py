# -*- coding: utf-8 -*-
""" Utils for path and URL """
import urllib


def safe_url(url):
    """ 转义包含非 ASCII 字符的 URL
    """
    parsed = urllib.parse.urlparse(url)
    safed = urllib.parse.ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=urllib.parse.quote(parsed.path),
        params=parsed.params,
        query=urllib.parse.urlencode(urllib.parse.parse_qsl(parsed.query)),
        fragment=parsed.fragment)
    return urllib.parse.urlunparse(safed)
