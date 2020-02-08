# 开发配置文档

如果无法运行 `shell` 脚本，请参考脚本内容自行处理。

## 准备环境配置

```shell
if [ ! -f .projrc ]; then
  # 复制模板
  cp scripts/base/environ.sample.rc .projrc

  # 指定当前目录为项目目录,也可手动设置（编辑第一行 PROJ_GIT_DIR=...）
  sed -i -e 1c"PROJ_GIT_DIR=$(pwd)" .projrc
fi
```

## 准备 `python` 环境

- 创建新的 pyenv 虚拟环境

  编辑 `.projrc` 中的 `PROJ_PYTHON_VER`、`PROJ_PYTHON_ENV`、`PROJ_PYTHON_BIN`，后调用：

  > ./scripts/host/02-pyenv.sh

- python 环境已就绪（无论是否虚拟）

  编辑 `.projrc` 中的 `PROJ_PYTHON`、`PROJ_PIP`

## 安装依赖

```shell
./scripts/dev/02-pip.sh
./scripts/base/02-pip.sh
./scripts/dev/40-submodules.sh
```

## 初始化项目配置及数据

自定义 `.projrc` 中其他配置，并执行：

```shell
./scripts/base/03-environ.sh
./scripts/dev/manage.sh migrate
./scripts/base/10-prepare.sh
```

如出现错误，修改 `.projrc` 中对应的键值，继续配置。

## 数据库变更(提交 PR 前必须重新合并)

```shell
./scripts/dev/40-makemigrations.sh
```

## 代码检查(提交 PR 前必须自检)

```shell
./scripts/dev/40-pylint.sh
```

## 单元测试(提交 PR 前必须自检)

```shell
./scripts/dev/40-tests.sh
```

## 合并业务、服务依赖(提交 PR 前必须执行)

```shell
./scripts/dev/40-requirements.sh
```

## 合并静态资源(如果项目需要，提交 PR 前必须执行)

```shell
./scripts/dev/manage.sh collectstatic --noinput
```

## 运行服务

```shell
./scripts/base/20-runserver.sh
```
