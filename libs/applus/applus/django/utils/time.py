# -*- coding: utf-8 -*-
""" Django Time Utils """
import datetime
from applus import time


def floor_before_time(before, unit):
    """ 转为本地时间，并清除精度 """
    before_time = time.date_or_time_to_local(before)
    #
    today_time = time.date_or_time_to_local(datetime.date.today())
    today_time = time.floor_time(today_time, unit)
    if not before_time:
        return today_time
    return min(today_time, time.floor_time(before_time, unit))

# 不同统计区间对应的丢弃精度
#   按天统计，丢弃时分秒
#   按月统计，丢弃时分秒，同时日期设为“1”
FLOOR_UNIT_OF_PERIODS = {
    # period: floor
    'day': 'hour',
    'month': 'day',
}

def next_count_range(count_date, period_unit):
    """ 下一次统计时间区间 """
    # 日期转换为本地时间
    count_time = time.date_to_datetime(count_date, local=True)
    # 起始时间丢弃精度
    floor_unit = FLOOR_UNIT_OF_PERIODS[period_unit]
    l_time = time.floor_time(count_time, floor_unit)
    # 当期已经统计过，起始时间往后推一期
    l_time = time.shift_period(l_time, period_unit)
    # 结束时间再推一期
    return l_time, time.shift_period(l_time, period_unit)


def near_count_range(origin_time, period_unit):
    """ 指定原始所在的统计时间区间 """
    # 转换为本地时间，依赖设置 django.conf.settings.TIME_ZONE
    origin_time = time.date_or_time_to_local(origin_time)
    # 起始时间丢弃精度
    floor_unit = FLOOR_UNIT_OF_PERIODS[period_unit]
    l_time = time.floor_time(origin_time, floor_unit)
    # 结束时间后推一期
    return l_time, time.shift_period(l_time, period_unit)


def get_range(latest_count, earliest_origin, period_unit):
    """ 计算新的统计时间区间 """
    # 最近的统计时间
    if callable(latest_count):
        latest_count = latest_count()
    if latest_count is not None:
        return next_count_range(latest_count, period_unit)
    # 没有统计过，获取第一条原始数据的时间
    if callable(earliest_origin):
        earliest_origin = earliest_origin()
    if not earliest_origin:
        return None, None
    return near_count_range(earliest_origin, period_unit)

# pylint: disable=too-many-arguments
def yield_range(latest_count, earliest_origin, period_unit, before_time):
    """ 遍历所有统计时间区间 """
    # 第一个统计区间
    l_time, r_time = get_range(latest_count, earliest_origin, period_unit)
    # 是否结束
    while l_time and r_time <= before_time:
        yield l_time, r_time
        # 移动区间
        l_time = r_time
        r_time = time.shift_period(r_time, period_unit)

############
# base DAO #
############

def get_first_time(dao, order_field, **kwargs):
    """ 最近的统计时间 """
    row = dao.filter(**kwargs).order_by(order_field).first()
    if row is None:
        return None
    #
    attr = order_field
    if attr[:1] in ['+', '-']:
        attr = attr[1:]
    return getattr(row, attr)
