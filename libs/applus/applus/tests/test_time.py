# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,no-self-use
import unittest
import datetime
from applus import time
from applus.django.time import (next_count_range, near_count_range)


__all__ = ['TestTime']


class TestTime(unittest.TestCase):

    def test_time(self):
        """ test time.py
        """
        now = time.now()
        str_of_day = now.date().isoformat()
        time.parse_date(str_of_day)
        str_of_time = now.time().isoformat()
        time.parse_time(str_of_time)
        str_of_now = now.isoformat()
        time.parse_datetime(str_of_now)
        #
        time.parse_duration(1)
        time.parse_duration('P1D')
        time.parse_duration('PT1H')
        time.parse_duration('03:00')

    def test_default_tz_offset(self):
        # 取决于 django.conf.settings : TIME_ZONE
        # 无法提供确定的测试用例, 请自行观测结果判断实现是否可靠
        #
        # ！！其他基于 localtime 的 API 测试用例依赖此函数！！
        pass

    def test_floor_date_to_datetime(self):
        tick = datetime.datetime(2019, 10, 24, 16, 47, 22)
        ##############
        # floor_time #
        ##############
        def floor(unit):
            return time.floor_time(tick, unit).isoformat()
        self.assertEqual('2019-10-24T16:47:00', floor('second'))
        self.assertEqual('2019-10-24T16:00:00', floor('minute'))
        self.assertEqual('2019-10-24T00:00:00', floor('hour'))
        self.assertEqual('2019-10-01T00:00:00', floor('day'))
        self.assertEqual('2019-01-01T00:00:00', floor('month'))
        self.assertEqual('2019-10-21T00:00:00', floor('weekday')) # 周一
        self.assertEqual('2019-10-20T00:00:00', floor('isoweekday')) # 周日
        with self.assertRaises(time.BaseTimeError) as exc:
            floor('year')
        self.assertEqual(str(exc.exception), "floor_time: unsupport unit<year>")
        ########################
        # floor_date(datetime) #
        ########################
        # pylint: disable=function-redefined
        def floor(unit):
            return time.floor_date(tick, unit).isoformat()
        with self.assertRaises(time.BaseTimeError) as exc:
            floor('hour')
        self.assertEqual(str(exc.exception), "floor_time: unsupport unit<hour>")
        self.assertEqual('2019-10-01', floor('day'))
        self.assertEqual('2019-01-01', floor('month'))
        self.assertEqual('2019-10-21', floor('weekday'))
        self.assertEqual('2019-10-20', floor('isoweekday'))
        with self.assertRaises(time.BaseTimeError) as exc:
            floor('year')
        self.assertEqual(str(exc.exception), "floor_time: unsupport unit<year>")
        ####################
        # floor_date(date) #
        ####################
        tick = datetime.date(2019, 10, 30) # 周三
        self.assertEqual('2019-10-01', floor('day'))
        self.assertEqual('2019-01-01', floor('month'))
        self.assertEqual('2019-10-28', floor('weekday')) # 周一
        self.assertEqual('2019-10-27', floor('isoweekday')) # 周日
        ####################
        # date_to_datetime #
        ####################
        day = datetime.date(2019, 10, 24)
        self.assertEqual('2019-10-24T00:00:00', time.date_to_datetime(day).isoformat())
        time_utc = time.date_to_datetime(day, utc=True)
        self.assertEqual('2019-10-24T00:00:00+00:00', time_utc.isoformat())
        #
        # local 取决于 django.conf.settings : TIME_ZONE, 测试用例无法预测输出
        offset = time.get_default_tz_offset()
        # 使用 offset 进行比较
        #
        time_loc = time.date_to_datetime(day, local=True) # '2019-10-24T00:00:00+08:06'
        self.assertEqual(offset, time_utc - time_loc)
        #

    def test_count_date_range(self):
        ################
        # shift_period #
        ################
        def shift(expect, tick, unit):
            self.assertEqual(expect, time.shift_period(tick, unit).isoformat())
        shift("2019-10-24", datetime.date(2019, 10, 24), "second")
        shift("2019-10-24", datetime.date(2019, 10, 24), "minute")
        shift("2019-10-24", datetime.date(2019, 10, 24), "hour")
        shift("2019-10-25", datetime.date(2019, 10, 24), "day")
        shift("2019-10-31", datetime.date(2019, 10, 24), "week")
        shift("2019-11-24", datetime.date(2019, 10, 24), "month")
        shift("2020-10-24", datetime.date(2019, 10, 24), "year")
        with self.assertRaises(ValueError) as exc:
            shift("", datetime.date(2019, 1, 31), "month")
        self.assertEqual(str(exc.exception), "day is out of range for month")
        with self.assertRaises(time.BaseTimeError) as exc:
            shift("", datetime.date(2019, 1, 31), "test")
        self.assertEqual(str(exc.exception), "shift_period: unsupport unit<test>")
        shift("2019-10-24T00:00:01", datetime.datetime(2019, 10, 24), "second")
        shift("2019-10-24T00:01:00", datetime.datetime(2019, 10, 24), "minute")
        shift("2019-10-24T01:00:00", datetime.datetime(2019, 10, 24), "hour")
        shift("2019-10-25T00:00:00", datetime.datetime(2019, 10, 24), "day")
        shift("2019-10-31T00:00:00", datetime.datetime(2019, 10, 24), "week")
        shift("2019-11-24T00:00:00", datetime.datetime(2019, 10, 24), "month")
        shift("2020-10-24T00:00:00", datetime.datetime(2019, 10, 24), "year")
        with self.assertRaises(ValueError) as exc:
            shift("", datetime.datetime(2019, 1, 31), "month")
        self.assertEqual(str(exc.exception), "day is out of range for month")
        with self.assertRaises(time.BaseTimeError) as exc:
            shift("", datetime.datetime(2019, 1, 31), "test")
        self.assertEqual(str(exc.exception), "shift_period: unsupport unit<test>")
        #########
        # range #
        #########
        # local 取决于 django.conf.settings : TIME_ZONE, 测试用例无法预测输出
        offset = time.get_default_tz_offset()
        # 使用 offset 进行比较
        #
        # 下一次统计时间区间
        date = datetime.date(2019, 10, 24)
        mint, maxt = next_count_range(date, 'day')
        # ['2019-10-25T00:00:00+08:00', '2019-10-26T00:00:00+08:00']
        #
        self.assertEqual(time.DAY, maxt - mint)
        date_utc = time.date_to_datetime(date, utc=True)
        # ('2019-10-24T00:00:00+00:00' OR '2019-10-24T08:00:00+08:00')
        #
        self.assertEqual(time.DAY + date_utc, mint + offset)
        #
        #
        # 指定原始所在的统计时间区间
        mint, maxt = near_count_range(date_utc, 'day')
        # ('2019-10-24T00:00:00+08:00', '2019-10-25T00:00:00+08:00')
        #
        self.assertEqual(time.DAY, maxt - mint)
        self.assertEqual((mint, maxt), near_count_range(time.localtime(date_utc), 'day'))
        #
        date_off = date_utc - offset - time.SECOND
        # '2019-10-23T15:59:59+00:00' OR '2019-10-23T23:59:59+08:00'
        #
        mino, maxt = near_count_range(date_off, 'day')
        # ('2019-10-23T00:00:00+08:00', '2019-10-24T00:00:00+08:00')
        #
        self.assertEqual(time.DAY, maxt - mino)
        self.assertEqual(time.DAY, mint - mino)
        #
