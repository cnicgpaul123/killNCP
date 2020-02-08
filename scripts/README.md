# 部署/开发文档

## 一键部署

- 编辑 `allinone.sh` 中相关配置

  `GIT` 配置

  - `PROJ_GIT_URL` 项目代码仓库
  - `PROJ_GIT_BRANCH` 版本(对应 git 中的分支名)
  - `PROJ_GIT_DIR` 存储位置

  环境配置的组织约定：按角色组织配置文件仓库：开发者各自维护，生产环境统一维护；每个仓库中包含该角色所能管理的所有项目环境配置，文件名统一规范：`GROUP/PROJ.rc`；分支代表运行环境(`prod`, `testing`, `development`)

  - `ENVIRON_RC` 环境配置文件路径: `/path/to/GROUP/PROJ.rc`
  - `ENVIRON_NAME` 运行环境名: `prod`
  - `ENVIRON_GIT` 环境配置文件仓库

  本部署脚本基于业务常用脚本的再组织而成，因此也需要适应业务脚本的运行环境，后续部署流程如下：

  - 获取/更新 GIT 代码
  - 输出环境配置（保证业务脚本可单独运行）
  - 应用项目环境配置
  - pyenv virtualenv 配置（根据环境设置智能处理）
  - 安装依赖
  - 更新项目配置
  - 更新服务配置
  - 启动/刷新服务

- 运行脚本
  `./scripts/allinone.sh`

## 脚本说明

- `.gitrc` 代码仓库配置

- `.projrc` 项目环境配置

- `scripts/base/` # 业务相关脚本

  | 脚本                | 说明                           |
  | ------------------- | ------------------------------ |
  | `02-pip.sh`         | 安装业务功能所需依赖           |
  | `03-environ.sh`     | 生成项目环境配置               |
  | `10-prepare.sh`     | 预处理数据                     |
  | `20-runserver.sh`   | 以 `django runserver` 启动服务 |
  | `environ.py.sh`     | `Django` 项目环境配置模板      |
  | `environ.sample.rc` | 环境变量配置模板               |
  | `requirements.txt`  | 业务功能所需依赖               |

- `scripts/deliver/` # 交付相关脚本

  | 脚本          | 说明                             |
  | ------------- | -------------------------------- |
  | `pack.sh`     | 交付打包脚本                     |
  | `sys-init.sh` | 交付部署手册对应的 OS 初始化脚本 |
  | `deploy.md`   | 部署&更新说明                    |

- `scripts/dev/` # 开发相关，与发布无关

  | 脚本                   | 说明                                              |
  | ---------------------- | ------------------------------------------------- |
  | `02-pip.sh`            | 安装开发所需依赖                                  |
  | `40-makemigrations.sh` | 数据库变更(提交 PR 前必须重新合并)                |
  | `40-pylint.sh`         | 语法检查（提交前检查）                            |
  | `40-requirements.sh`   | 合并业务、运行所需依赖（可选，提交前检查）        |
  | `40-submodules.sh`     | 以 `python setup.py --develop` 方式注册子模块依赖 |
  | `40-tests.sh`          | 单元测试（提交前处理）                            |
  | `env.sh`               | `pyenv` 环境下，无需激活(activate)相关环境        |
  | `manage.sh`            | `pyenv` 环境下，无需激活(activate)相关环境        |
  | `requirements.txt`     | 开发所需依赖                                      |

- `scripts/host/` # 服务相关脚本

  | 脚本               | 说明                                                   |
  | ------------------ | ------------------------------------------------------ |
  | `00-git-clone.sh`  | 仅用于克隆项目，需要准备 `.gitrc` & `.projrc` 配置文件 |
  | `01-git-update.sh` | 更新到指定分支                                         |
  | `02-pip.sh`        | 安装服务运行所需依赖                                   |
  | `02-pyenv.sh`      | 安装 pyenv 虚拟环境（可配、可选）                      |
  | `19-nginx.sh`      | 生成 nginx include 配置                                |
  | `19-nuxt.sh`       | 编译 nuxt                                              |
  | `19-supervisor.sh` | 生成 supervisor include 配置                           |
  | `19-uwsgi.sh`      | 生成 uwsgi 配置                                        |
  | `20-runserver.sh`  | 以自定义方式启动服务: `uwsgi`, `gunicorn`, ...         |
  | `requirements.txt` | 服务运行所需依赖                                       |
