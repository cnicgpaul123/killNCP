# pylint: disable=missing-docstring,no-self-use
import unittest
import pytz
from celery.utils import time
from celery import schedules


__all__ = ['TestCelery']


class TestCelery(unittest.TestCase):
    """ celery 测试
    """

    def test_crontab(self):
        """ celery crontab 测试
        """
        pytz.timezone('Asia/Shanghai')
        time.datetime(2019, 1, 14, 15, 22, 14, 160608)
        schedules.crontab(minute='*/1')
