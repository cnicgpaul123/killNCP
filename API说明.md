#### 1.判断第一次还是第二次填写信息
```
http://159.226.29.113:8000/api/personinfoiscreate/
post请求
请求数据内容(json格式)：{"phone": "13580558370", "userid": "xxx"}
# userid是用户登录后，前端获取到userid，然后请求我这个接口时带上这个userid(userid是唯一的)

返回响应：
{
    "flag": 1, #flag为1，则是第二次填，为0则是第一次填，为2则是后台没接收phone字段数据
    "name": "程三",
    "idcard": "440811199302082378",
    "carid": "粤A412355",
    "phone": "13580558370",
    "is_local": true,
    "is_fromhubei": false,
    "comefrom": "广东湛江",
    "travel_mode": 1,
    "springtime": "2020-02-11T06:53:00Z",
    "add_time": "2020-02-11T09:54:00Z",
    "desc": "无",

    "userid": "xxx"   # 属于哪个账号
}
或
{"flag": 0}
或
{"flag": 2}
```

#### 2.（在第二次填写信息的情况）填写到访信息
```
http://159.226.29.113:8000/api/visitinfo/
post请求
请求数据内容(json格式)：
{
    "phone": "13580558370",  #本人
    "contactname": "房东1", # 本单位联系人姓名
    "contactphone": "13580558369", # 本单位联系人电话
    "reason": "住宿",         # 到访事由
    "temperature": "36.5"   # 测得体温

    "userid": "xxx"   # 属于哪个账号
}

返回响应：
200（即提交成功）
```

#### 3.（在第一次填写信息的情况）填写人员信息
```
http://159.226.29.113:8000/api/personinfo/
post请求
请求数据内容(json格式)：
{
    "name": "李四",
    "idcard": "440811199308022376",
    "carid": "粤A123456",
    "phone": "13580558370",  #本人
    "is_local": 1, # 1为是本地户籍，0为不是本地户籍
    "is_fromhubei": 0, # 1为来自湖北，0则相反
    "comefrom": "广东湛江", # 来源地区
    "travel_mode": 1, # 1为火车，2为自驾，3为汽车，4为飞机
    "springtime": "2020-02-11 13:51:24" # 春运时间
    "desc": "无"，   # 备注说明情况

    "contactname": "房东1", # 本单位联系人姓名
    "contactphone": "13580558369", # 本单位联系人电话
    "reason": "住宿",         # 到访事由
    "temperature": "36.5"   # 测得体温

    "userid": "xxx"   # 属于哪个账号
}

返回响应：
201（即提交成功）

get请求
http://159.226.29.113:8000/api/personinfo/?userid="xxxx" # 请注意一定要加userid字段
{
    "count": 8,
    "next": "http://159.226.29.113:8000/api/personinfo/?page=2",
    "previous": null,
    "results": [
        {
            "id": 12,
            "visitinfo": [     # [ ]里的是到访信息
                {
                    "id": 13,
                    "contactname": "严防东",
                    "contactphone": "13580558379",
                    "reason": "务工住宿",
                    "temperature": "34.9",
                    "add_time": "2020-02-14 13:33:41",
                    "person_id": 12
                },
                {
                    "id": 12,
                    "contactname": "王房东",
                    "contactphone": "13702479565",
                    "reason": "探亲",
                    "temperature": "36.9",
                    "add_time": "2020-02-14 12:29:55",
                    "person_id": 12
                }
            ],
            "name": "严谨静",   # 从这开始以下字段是人员信息
            "idcard": "440811199202082376",
            "carid": "粤A412153",
            "phone": "13512358364",
            "is_local": true,
            "is_fromhubei": false,
            "comefrom": "广东阳江",
            "travel_mode": 1,
            "springtime": "2020-02-14 12:28:00",
            "add_time": "2020-02-14 12:29:55",
            "desc": "无"
        },
}
```

#### 4.搜索接口（搜名字或手机）
```
http://159.226.29.113:8000/api/personinfo/?search=程&userid="xxxx"    # 请注意一定要加userid字段
或http://159.226.29.113:8000/api/personinfo/?search=135805&userid="xxxx"  # 请注意一定要加userid字段
get请求

比如：http://159.226.29.113:8000/api/personinfo/?search=58367&userid="xxxx" # 请注意一定要加userid字段
返回响应：
200（即搜索成功）
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "visitinfo": [             # [ ]里的是到访信息
                {
                    "id": 1,
                    "contactname": "林房东",
                    "contactphone": "13580559632",
                    "reason": "住宿",
                    "temperature": "36.3",
                    "add_time": "2020-02-13 17:35:17",
                    "person_id": 1
                }
            ],
            "name": "李四",          # 从这开始以下字段是人员信息
            "idcard": "440811199302082375",
            "carid": "粤A412352",
            "phone": "13580558367",  # 搜索手机号search=58367
            "is_local": true,
            "is_fromhubei": true,
            "comefrom": "广东河源",
            "travel_mode": 2,
            "springtime": "2020-02-11 13:51:24",
            "add_time": "2020-02-11 13:52:14",
            "desc": "无"
        }
    ]
}
```

#### 5.导出excel接口
```
http://159.226.29.113:8000/api/exportexcel/?userid="xxxx"
get请求

返回响应：
200（即搜索成功）
```
