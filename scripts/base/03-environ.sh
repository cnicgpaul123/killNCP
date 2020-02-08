# 环境变量
. .projrc

# 工作目录
cd ${PROJ_GIT_DIR}

# 项目配置
. scripts/base/environ.py.sh

# 日志目录
mkdir -p ${PROJ_LOG_DIR}

# 动态目录
# mkdir -p ${MEDIA_ROOT}

# 收集静态资源存至指定目录(部署时处理)
${PROJ_PYTHON} manage.py collectstatic --noinput
