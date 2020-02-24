# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
# from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.models import User

from datetime import datetime
import xlwt
from io import BytesIO

from .models import PersonInfo, VisitInfo
from .serializers import PersonInfoSerializer


class PersonInfoIsCreateView(APIView):
    # 判断第一次还是第二次填写信息
    def post(self, request):
        phone = request.data.get("phone", None)
        userid = request.data.get("userid", None)
        if phone is not None and userid is not None:
            personinof_obj = PersonInfo.objects.filter(phone=phone, userid=userid).first()
            if personinof_obj:
                data = dict()
                data["flag"] = 1
                data["name"] = personinof_obj.name
                data["idcard"] = personinof_obj.idcard
                data["carid"] = personinof_obj.carid
                data["phone"] = personinof_obj.phone
                data["is_local"] = personinof_obj.is_local
                data["is_fromhubei"] = personinof_obj.is_fromhubei
                data["comefrom"] = personinof_obj.comefrom
                data["travel_mode"] = personinof_obj.travel_mode
                data["springtime"] = personinof_obj.springtime
                data["add_time"] = personinof_obj.add_time
                data["desc"] = personinof_obj.desc
                data["userid"] = personinof_obj.userid
                return Response(data)
            else:
                return Response({"flag": 0, "phone": phone})
        else:
            return Response({"flag": 2})


class VisitInfoCreateView(APIView):
    #（在第二次填写信息的情况）填写到访信息
    def post(self, request):
        phone = request.data.get("phone", None)
        contactname = request.data.get("contactname", None)
        contactphone = request.data.get("contactphone", None)
        reason = request.data.get("reason", None)
        temperature = request.data.get("temperature", None)
        userid = request.data.get("userid", None)

        personinof_obj = PersonInfo.objects.filter(phone=phone, userid=userid).first()

        VisitInfo.objects.create(contactname=contactname, contactphone=contactphone, \
                                reason=reason, temperature=temperature, person_id=personinof_obj)
        return Response({"msg": "ok"})


class PersonInfoPagination(PageNumberPagination):
    page_size = 10                   # 表示每页的默认显示数量
    page_size_query_param = "size"  # 表示url中每页数量参数
    page_query_param = "page"       # 表示url中的页码参数
    max_page_size = 100             # 表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃


class PersonInfoViewSet(viewsets.ModelViewSet):
    """
    人员信息,增删改查
    列表页, 分页， 搜索， 过滤， 排序
    """
    queryset = PersonInfo.objects.all()
    serializer_class = PersonInfoSerializer
    # pagination_class = PersonInfoPagination
    # permission_classes = [permissions.IsAdminUser]
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (filters.SearchFilter, ) # filters.DjangoFilterBackend, filters.OrderingFilter,
    # filter_class = PersonInfoFilter
    search_fields = ('name', 'phone')   
    # ordering_fields = ('add_time', )

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.IsAdminUser()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        contactname = request.data.get("contactname", None)
        contactphone = request.data.get("contactphone", None)
        reason = request.data.get("reason", None)
        temperature = request.data.get("temperature", None)
        userid = request.data.get("userid", None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        personinof_obj = PersonInfo.objects.filter(phone=phone, userid=userid).first()
        VisitInfo.objects.create(contactname=contactname, contactphone=contactphone, \
                                reason=reason, temperature=temperature, person_id=personinof_obj)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        userid = request.query_params["userid"]

        # queryset = PersonInfo.objects.filter(userid=userid)
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = self.filter_queryset(PersonInfo.objects.filter(userid=userid))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ExportExcelView(APIView):
    """
    导出人员信息excel表
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        
        travel_type = {"1":"火车", "2":"自驾", "3":"汽车", "4":"飞机"}
        now = datetime.now()
        time = datetime.strftime(now, '%Y%m%d%H%M%S')
        # 设置excel文件名
        filename = time+'.xls'

        # 设置HTTPResponse的类型
        reposnse = HttpResponse(content_type='application/vnd.ms-excel')
        # 创建一个文件对象
        reposnse['Content-Disposition'] = 'attachment;filename='+filename

        # 创建一个sheet对象
        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet('PersonInfo-sheet')
        # 写入文件标题
        sheet.write(0, 0, '姓名')
        sheet.write(0, 1, '身份证号')
        sheet.write(0, 2, '车牌号')
        sheet.write(0, 3, '联系电话')
        sheet.write(0, 4, '是否本地户籍')
        sheet.write(0, 5, '是否来自湖北')
        sheet.write(0, 6, '来源地区')
        sheet.write(0, 7, '春运出行方式')
        sheet.write(0, 8, '抵达本地时间')
        # sheet.write(0, 9, '联系人姓名')
        # sheet.write(0, 10, '联系人电话')
        # sheet.write(0, 11, '到访事由')
        # sheet.write(0, 12, '记录体温')
        sheet.write(0, 9, '添加时间')
        sheet.write(0, 10, '现居住')
        sheet.write(0, 11, '账号')
        data_row = 1

        userid = request.GET["userid"]

        for person in PersonInfo.objects.filter(userid=userid).order_by('add_time'):
            sheet.write(data_row, 0, person.name)
            sheet.write(data_row, 1, person.idcard)
            sheet.write(data_row, 2, person.carid)
            sheet.write(data_row, 3, person.phone)
            if person.is_local == True:
                    islocal = "是"
            else:
                    islocal = "否"
            sheet.write(data_row, 4, islocal)

            if person.is_fromhubei == True:
                    isfromhubei = "是"
            else:
                    isfromhubei = "否"
            sheet.write(data_row, 5, isfromhubei)

            sheet.write(data_row, 6, person.comefrom)
            
            sheet.write(data_row, 7, travel_type[str(person.travel_mode)])
            
            sheet.write(data_row, 8, str(person.springtime))
            # sheet.write(data_row, 9, person.contactname)
            # sheet.write(data_row, 10, person.contactphone)
            # sheet.write(data_row, 11, person.reason)
            # sheet.write(data_row, 12, person.temperature)
            sheet.write(data_row, 9, str(person.add_time))
            sheet.write(data_row, 10, person.desc)

            obj = User.objects.filter(id=person.userid).first()
            sheet.write(data_row, 11, obj.username)
            
            data_row = data_row + 1

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        reposnse.write(output.getvalue())

        return reposnse
