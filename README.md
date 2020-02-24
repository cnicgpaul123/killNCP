## 疫情防控-出入人员登记系统

- 本出入人员登记系统由广州中科院计算机网络信息中心党支部技术团队开发，可自由免费的使用项目源码，包括前端和后端。
- 前端基于VUE，h5网页
- 后端基于Django rest framework。
- 感谢中国科技云提供免费服务器资源支持，该系统已部署在科技云，项目体验地址：http://dengji.fangyi.cniotroot.cn/
- 感谢广州中科院计算机网络信息中心党支部开发人员
- 技术支持: QQ: 562029186

### django rest framework + uwsgi + nginx 方式部署

#### 1.准备环境配置(在项目根目录创建shell脚本文件，执行该脚本将生成.projrc配置文件)

```shell
if [ ! -f .projrc ]; then
  # 复制模板
  cp scripts/base/environ.sample.rc .projrc

  # 指定当前目录为项目目录,也可手动设置（编辑第一行 PROJ_GIT_DIR=...）
  sed -i -e 1c"PROJ_GIT_DIR=$(pwd)" .projrc
fi
```

#### 2.准备 `python` 环境

- 创建新的 pyenv 虚拟环境

  编辑 `.projrc` 中的 `PROJ_PYTHON_VER`、`PROJ_PYTHON_ENV`、`PROJ_PYTHON_BIN`，后调用：

  > ./scripts/host/02-pyenv.sh

- 也可以创建 virtualenv 虚拟环境

  编辑 `.projrc` 中的 `PROJ_PYTHON_VER`、`PROJ_PYTHON_ENV`、`PROJ_PYTHON_BIN`、`PROJ_PYTHON`、`PROJ_PYTHON`，指定python版本，虚拟环境下的python和pip


- python 环境已就绪（无论是否虚拟）

  编辑 `.projrc` 中的 `PROJ_PYTHON`、`PROJ_PIP`

#### 3.安装依赖包

```shell
./scripts/dev/02-pip.sh
./scripts/base/02-pip.sh
./scripts/dev/40-submodules.sh
```

#### 4.初始化项目配置及数据

自定义 `.projrc` 中其他配置，并执行：

```shell
./scripts/base/03-environ.sh
./scripts/dev/manage.sh migrate
./scripts/base/10-prepare.sh
```
如出现错误，修改 `.projrc` 中对应的键值，继续配置。

#### 5.运行服务

```shell
./scripts/base/20-runserver.sh
```

#### 6.如果数据库有变更，执行如下脚本

```shell
./scripts/dev/40-makemigrations.sh
```

#### 7.uwsgi配置文件
```
[uwsgi]
chdir=/home/paul/kill_NCP_ci_fronted/killNCP  # 项目根目录
module=wsgi:application
master=true
processes=4
socket=127.0.0.1:8082                         # 指定内部端口8082，也可自定义
vacuum=true
virtualenv=/home/paul/kill_NCP_ci_fronted/venv_killncp_ci_fronted # 指定虚拟环境目录
```

#### 8.nginx配置文件
```
server {
    # use for killncp_fronted
    listen 80;
    server_name 0.0.0.0;

    # uploads max file
    client_max_body_size 20m;

    access_log /home/paul/kill_NCP_ci_fronted/killNCP/logs/killncp_access.log;
    error_log /home/paul/kill_NCP_ci_fronted/killNCP/logs/killncp_error.log;       
    
    location / {
        # 前端文件存放的目录路径
        root /home/paul/kill_NCP_ci_fronted/killNCP/www/nconv2019/dist;
        index index.html index.htm;

        #include uwsgi_params;
        #uwsgi_pass 127.0.0.1:8082;
        #uwsgi_param UWSGI_CHDIR /home/paul/kill_NCP_ci_fronted/killNCP;
        #uwsgi_param UWSGI_SCRIPT manage:app;
    }

    location ~ /(api) {
         include uwsgi_params;
         uwsgi_pass 127.0.0.1:8082;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {                                                                            
        root   /usr/share/nginx/html;        
    }
}

```

### 本地测试

#### 1.创建一个/environ/ python包，新建default.py文件
```
default.py(可根据setting.py的内容进行自定义更改)，例如：

DEBUG = True # setting.py中的DEBUG=False,可在defauly.py中自定义设置为True

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "killncp",
        'USER': 'root',
        'PASSWORD': "xxxxxxxx",
        'HOST': "127.0.0.1",
        'PORT': "3306",
        # 'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' }
    }
}
```
#### 2.执行以下命令，启动服务
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
