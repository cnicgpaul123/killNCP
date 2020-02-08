# 部署&更新

## 前置要求

- 请用 `maintain` 用户运行该脚本
- 配置 `sudo useradd -G wheel maintain`

## 目录结构

```shell
[ ! -d /cnicg ] && sudo mkdir /cnicg && sudo chown maintain:maintain /cnicg
mkdir -p /cnicg/{conf,projs,logs,downloads} /cnicg/conf/{nginx,supervisor}/conf.d
```

## 获取版本并解压

```shell
# 解压当前版本
tar -xzf /cnicg/downloads/PRODUCT-VERSION.tar.gz -C /cnicg/projs/

# 固定路径软连接
rm -f /cnicg/projs/PRODUCT && ln -s /cnicg/projs/PRODUCT-VERSION.tar.gz /cnicg/projs/PRODUCT
```

## 依赖服务/应用配置

```shell
# $ mysql -P3306 -uroot -p
# MariaDB [(none)]> create database db_NAME charset utf8;
```

## 初始化环境变量

```shell
cd /cnicg/projs/PRODUCT && mkdir -p .data

cp scripts/base/environ.sample.rc .projrc
```

## 编辑 .projrc 中的环境变量

```shell
# 数据库连接配置
# DB_URI="mysql://USERNAME:PASSWORD@127.0.0.1:3306/db_NAME?charset=utf8"
```

## 应用环境变量

```shell
./scripts/flush.sh

# 更新数据库结构
# ./scripts/dev/manage.sh migrate

# 创建初始超级用户
# ./scropts/dev/manage.sh createsuperuser
```

## 刷新 supervisor

```shell
rm -f /cnicg/conf/supervisor/conf.d/PRODUCT.conf && ln -s /cnicg/projs/PRODUCT/scripts/host/supervisor.conf /cnicg/conf/supervisor/conf.d/PRODUCT.conf
sudo supervisorctl update
sudo supervisorctl restart PRODUCT:*
```

## 刷新 nginx

```shell
rm -f /cnicg/conf/nginx/conf.d/PRODUCT.conf && ln -s /cnicg/projs/PRODUCT/scripts/host/nginx.conf /cnicg/conf/nginx/conf.d/PRODUCT.conf
sudo nginx -t
sudo nginx -s reload
```
