# -*- coding: utf-8 -*-
__author__ = 'chengmengbao'

from django.db import models
from datetime import datetime
import django.utils.timezone as timezone
# Create your models here.


class PersonInfo(models.Model):
    """
    人员信息：
        - 姓名
        - 身份证号
        - 车牌号
        - 联系电话
        - 是否本地户籍
        - 是否来自湖北
        - 来源地区
        - 春运出行方式（火车，自驾，汽车，飞机）
        - 春运日期
        - 添加时间
        - 备注情况
    """
    TRAVEL_TYPE = (
        ("0", "无"),
        ("1", "火车"),
        ("2", "自驾"),
        ("3", "汽车"),
        ("4", "飞机"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="姓名", help_text="姓名")
    idcard = models.CharField(default="", max_length=30, unique=True, verbose_name="身份证号", help_text="身份证号")
    carid = models.CharField(default="无", max_length=30, verbose_name="车牌号", help_text="车牌号")
    phone = models.CharField(default="", max_length=13, unique=True, verbose_name="联系电话", help_text="联系电话")
    is_local = models.BooleanField(default=False, verbose_name="是否本地户籍", help_text="是否本地户籍")
    is_fromhubei = models.BooleanField(default=False, verbose_name="是否来自湖北", help_text="是否来自湖北")
    comefrom = models.CharField(default="", max_length=30, verbose_name="来源地区", help_text="来源地区")
    travel_mode = models.CharField(default="0", max_length=8, choices=TRAVEL_TYPE, verbose_name="春运出行方式", help_text="春运出行方式")
    springtime = models.DateTimeField(default=timezone.now, verbose_name="抵达本地时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    desc = models.TextField(default="", verbose_name="现居住", help_text="现居住")

    userid = models.CharField(default="", max_length=30, verbose_name="账号", help_text="账号")

    class Meta:
        ordering = ['-add_time']
        verbose_name = "出入人员登记表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class VisitInfo(models.Model):
    """
    到访信息：
        - 本单位联系人姓名
        - 联系人电话
        - 到访事由
        - 记录体温
    """
    contactname = models.CharField(default="", max_length=30, verbose_name="本单位联系人姓名", help_text="本单位联系人姓名")
    contactphone = models.CharField(default="", max_length=13, verbose_name="联系人电话", help_text="联系人电话")
    reason = models.TextField(default="", verbose_name="到访事由", help_text="到访事由")
    temperature = models.CharField(default="", max_length=13, verbose_name="记录体温", help_text="记录体温")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    person_id = models.ForeignKey("PersonInfo", null=True, blank=True, related_name="visitinfo", on_delete=models.CASCADE, verbose_name="出入人员信息")

    class Meta:
        ordering = ['-add_time']
        verbose_name = "到访信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.contactname
