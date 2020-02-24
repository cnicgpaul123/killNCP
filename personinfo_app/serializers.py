# -*- coding: utf-8 -*-
__author__ = 'chengmengbao'

from rest_framework import serializers

from .models import PersonInfo, VisitInfo


class VisitInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitInfo
        fields = "__all__"


class PersonInfoSerializer(serializers.ModelSerializer):
    visitinfo = VisitInfoSerializer(many=True, read_only=True)

    contactname = serializers.CharField(write_only=True, help_text="本单位联系人姓名")
    contactphone = serializers.CharField(write_only=True, help_text="联系人电话")
    reason = serializers.CharField(write_only=True, help_text="到访事由")
    temperature = serializers.CharField(write_only=True, help_text="记录体温")

    carid = serializers.CharField(allow_blank=True, allow_null=True, help_text="车牌号")
    desc = serializers.CharField(allow_blank=True, allow_null=True, help_text="现居住")
    travel_mode = serializers.CharField(allow_blank=True, allow_null=True, help_text="春运出行方式")
    # springtime = serializers.DateTimeField(allow_blank=True, allow_null=True, help_text="春运日期")

    def validate(self, attrs):
        del attrs["contactname"]
        del attrs["contactphone"]
        del attrs["reason"]
        del attrs["temperature"]
        return attrs

    class Meta:
        model = PersonInfo
        fields = "__all__"


