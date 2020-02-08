# pylint: disable=missing-docstring,no-self-use
import unittest
from applus import time


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
