# -*- coding: utf-8 -*-
""" base on django """
import datetime
import functools
import django.utils.timezone
import django.utils.dateparse


ZERO = datetime.timedelta(0)
SECOND = datetime.timedelta(seconds=1)
MINUTE = datetime.timedelta(minutes=1)
HOUR = datetime.timedelta(hours=1)
DAY = datetime.timedelta(days=1)
WEEK = datetime.timedelta(days=7)

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


@functools.lru_cache()
def get_default_timezone():
    """ django.timezone & pytz.DstTzInfo 有些古怪
    #
    tz = timezone.get_current_timezone()
    # <DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>
    #
    datetime.datetime(*datetime.date.today().timetuple()[:4], tzinfo=tz)
    # datetime.datetime(2019, 10, 25, 0, 0, tzinfo=<DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>)
    #
    #
    tz2 = timezone.localtime(timezone.now()).tzinfo
    # now: datetime.datetime(..., tzinfo=<UTC>)
    # localtime: datetime.datetime(..., tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
    # <DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>
    #
    datetime.datetime(*datetime.date.today().timetuple()[:4], tzinfo=tz2)
    # datetime.datetime(2019, 10, 25, 0, 0, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
    """
    now_t = django.utils.timezone.now()
    now_l = django.utils.timezone.localtime(now_t)
    return now_l.tzinfo


def localtime(value=None, timezone=None):
    """ Convert an aware datetime.datetime to local time. """
    return django.utils.timezone.localtime(value, timezone)


@functools.lru_cache()
def get_default_tz_offset():
    """ 获取默认时区与 UTC 的偏移 """
    now_t = datetime.datetime.now()
    now_l = now_t.replace(tzinfo=get_default_timezone())
    now_u = now_t.replace(tzinfo=django.utils.timezone.utc)
    return now_u - now_l

########
# 扩展 #
########

def date_to_datetime(date, **kwargs):
    """ 日期转换为时间

    d = datetime.date.today() # '2019-10-24'
    #  list(d.timetuple()) # [2019, 10, 24, 0, 0, 0, 3, 297, -1]
    datetime.datetime(*d.timetuple()[:4]) # datetime.datetime(2019, 10, 24, 0, 0)
    datetime.datetime(*d.timetuple()[:4], tzinfo=utc).isoformat() # '2019-10-24T00:00:00+00:00'
    """
    tup = date.timetuple()[:4]
    if kwargs.pop('utc', False):
        kwargs['tzinfo'] = TZ_UTC
    if kwargs.pop('local', False):
        kwargs['tzinfo'] = get_default_timezone()
    return datetime.datetime(*tup, **kwargs)

# list(t.timetuple()) ==> [2019, 10, 24, 16, 31, 45, 3, 297, -1]
TIMETUPLE_UNITS = ['year', 'month', 'day', 'hour', 'minute', 'second']

EXTRA_UNITS = ['weekday', 'isoweekday']

DURATION_UNITS = {
    'second': SECOND,
    'minute': MINUTE,
    'hour': HOUR,
    'day': DAY,
    'week': WEEK,
}


def floor_date(time, unit):
    """
    t = datetime.datetime.now()
    # '2019-10-24T16:47:22.432626' 周四
    # [2019, 10, 24, 16, 47, 22, 3, 297, -1]

    floor_date(time, 'hour')       # BaseTimeError: ('floor_date: unsupport unit<hour>')
    floor_date(time, 'day')        # '2019-10-01'
    floor_date(time, 'month')      # '2019-01-01'
    floor_date(time, 'year')       # BaseTimeError: ('floor_date: unsupport unit<year>')
    #
    floor_date(time, 'weekday')    # '2019-10-21' 周一
    floor_date(time, 'isoweekday') # '2019-10-20' 周日
    """
    # 也支持 datetime 时间
    if isinstance(time, datetime.datetime):
        time = time.date()
    ########################
    # 扩展支持以星期为单位 #
    ########################
    if unit == 'weekday':
        return time - DAY * time.weekday()
    if unit == 'isoweekday':
        return time - DAY * time.isoweekday()
    ############
    # 简单处理 #
    ############
    try:
        unit_index = TIMETUPLE_UNITS.index(unit)
    except ValueError:
        pass
    else:
        tup = list(time.timetuple())[:unit_index]
        # 月/日：至少需要三个参数，自动补齐
        if unit in ['month', 'day']:
            tup.extend([1] * (3 - len(tup)))
            return datetime.date(*tup)
    ##########
    # 不支持 #
    ##########
    raise BaseTimeError("floor_time: unsupport unit<%s>" % unit)


def floor_time(time, unit):
    """
    time = datetime.datetime.now()
    # '2019-10-24T16:47:22.432626' 周四
    # [2019, 10, 24, 16, 47, 22, 3, 297, -1]

    floor_time(time, 'second')     # '2019-10-24T16:47:00'
    floor_time(time, 'minute')     # '2019-10-24T16:00:00'
    floor_time(time, 'hour')       # '2019-10-24T00:00:00'
    floor_time(time, 'day')        # '2019-10-01T00:00:00'
    floor_time(time, 'month')      # '2019-01-01T00:00:00'
    floor_time(time, 'year')       # BaseTimeError: ('floor_time: unsupport unit<year>')
    #
    floor_time(time, 'weekday')    # '2019-10-21T00:00:00' 周一
    floor_time(time, 'isoweekday') # '2019-10-20T00:00:00' 周日
    """
    ########################
    # 扩展支持以星期为单位 #
    ########################
    if unit == 'weekday':
        return floor_time(time, 'hour') - DAY * time.weekday()
    if unit == 'isoweekday':
        return floor_time(time, 'hour') - DAY * time.isoweekday()
    ############
    # 简单处理 #
    ############
    try:
        unit_index = TIMETUPLE_UNITS.index(unit)
    except ValueError:
        pass
    else:
        tup = list(time.timetuple())[:unit_index]
        # 时/分/秒
        if unit in ['hour', 'minute', 'second']:
            return datetime.datetime(*tup, tzinfo=time.tzinfo)
        # 月/日：至少需要三个参数，自动补齐
        if unit in ['month', 'day']:
            tup.extend([1] * (3 - len(tup)))
            return datetime.datetime(*tup, tzinfo=time.tzinfo)
    ##########
    # 不支持 #
    ##########
    raise BaseTimeError("floor_time: unsupport unit<%s>" % unit)


def date_or_time_to_local(date_or_time):
    """ 日期/时间 转换为本地时间 """
    if isinstance(date_or_time, datetime.datetime):
        return localtime(date_or_time)
    if isinstance(date_or_time, datetime.date):
        return date_to_datetime(date_or_time, local=True)
    return None


def shift_period(date_or_time, unit, count=1):
    """ 统计时间区间移动

    注意：请自行处理 date_or_time 为区间的左边界，错误示例:

    - shift_period("2019-01-30", "month", 1) ==> "2019-02-30"(无效时间)
    """
    if unit in DURATION_UNITS:
        return date_or_time + count * DURATION_UNITS[unit]
    if unit == 'month':
        year = date_or_time.year
        month = date_or_time.month + count
        while month < 1:
            year -= 1
            month += 12
        while month > 12:
            year += 1
            month -= 12
        return date_or_time.replace(year=year, month=month)
    if unit == 'year':
        year = date_or_time.year
        return date_or_time.replace(year=year+count)
    ##########
    # 不支持 #
    ##########
    raise BaseTimeError("shift_period: unsupport unit<%s>" % unit)


def fix_between_right(date_or_time):
    """  expr BETWEEN min AND max
    If expr is greater than or equal to min and expr is less than or equal to max,
        BETWEEN returns 1, otherwise it returns 0.
    This is equivalent to the expression (min <= expr AND expr <= max) ...

    See more: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html

    Example:

    range = (datetime.date(2019, 11, 3), datetime.date(2019,11,5))
    row in queryset.filter(date__range=range):
        print(row.date)
    #
    # 2019-11-03
    # 2019-11-05
    """
    if isinstance(date_or_time, datetime.datetime):
        return date_or_time - SECOND
    return date_or_time - DAY
