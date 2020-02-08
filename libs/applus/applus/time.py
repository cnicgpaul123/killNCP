# -*- coding: utf-8 -*-
""" base on django
"""
import datetime
import django.utils.timezone
import django.utils.dateparse


ZERO = datetime.timedelta(0)

TZ_UTC = django.utils.timezone.utc


class BaseTimeError(Exception):
    """ 时间错误基类 """


class DateParseError(BaseTimeError):
    """ date 解析错误 """


class TimeParseError(BaseTimeError):
    """ time 解析错误 """


class DateTimeParseError(BaseTimeError):
    """ datetime 解析错误 """


class DurationParseError(BaseTimeError):
    """ timedelta 解析错误 """


def now():
    """ 获取UTC当前时间。

    :rtype: datetime(with UTC)
    """
    return datetime.datetime.utcnow().replace(tzinfo=TZ_UTC)


def format_localtime(formatter='%Y%m%d-%H%M%S', local_time=None):
    """ 格式化本地时间
    """
    if not local_time:
        local_time = datetime.datetime.now()
    return local_time.strftime(formatter)


def parse_date(value):
    """Parses a value and return a datetime.date.

    Raises DateParseError if the input is well formatted but not a valid date.
    Returns None if the input isn't well formatted.
    """
    if isinstance(value, datetime.date):
        return value
    if not isinstance(value, str):
        raise DateParseError(
            'value must be instance of date or string'
            ', but given {}'.format(value.__class__))
    ret = django.utils.dateparse.parse_date(value)
    if ret:
        return ret
    raise DateParseError('cant parse `{}` to date'.format(value))


def parse_time(value):
    """Parses a value and return a datetime.time.

    This function doesn't support time zone offsets.

    Raises TimeParseError if the input is well formatted but not a valid time.
    Returns None if the input isn't well formatted, in particular if it
    contains an offset.
    """
    if isinstance(value, datetime.time):
        return value
    if not isinstance(value, str):
        raise TimeParseError(
            'value must be instance of time or string'
            ', but given {}'.format(value.__class__))
    ret = django.utils.dateparse.parse_time(value)
    if ret:
        return ret
    raise TimeParseError('cant parse `{}` to time'.format(value))


def parse_datetime(value):
    """Parses a value and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raises DateTimeParseError if the input is well formatted but not a valid datetime.
    Returns None if the input isn't well formatted.
    """
    if isinstance(value, datetime.datetime):
        return value
    if not isinstance(value, str):
        raise DateTimeParseError(
            'value must be instance of datetime or string'
            ', but given {}'.format(value.__class__))
    ret = django.utils.dateparse.parse_datetime(value)
    if ret:
        return ret
    raise DateTimeParseError('cant parse `{}` to datetime'.format(value))


def parse_duration(value, period='seconds'):
    """Parses a value and returns a datetime.timedelta.

    The preferred format for durations in Django is '%d %H:%M:%S.%f'.

    Also supports ISO 8601 representation.
    """
    if isinstance(value, datetime.timedelta):
        return value
    if isinstance(value, (int, float)):
        return datetime.timedelta(**{period: value})
    if not isinstance(value, str):
        raise DurationParseError(
            'value must be instance of timedelta'
            ', number or string, but given {}'.format(value.__class__))
    ret = django.utils.dateparse.parse_duration(value)
    if isinstance(ret, datetime.timedelta):
        return ret
    raise DurationParseError('cant parse `{}` to duration'.format(value))
