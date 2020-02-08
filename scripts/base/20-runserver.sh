# 环境变量
. .projrc

# 设定工作目录
cd ${PROJ_GIT_DIR}

# 启动服务(http)
${PROJ_PYTHON} manage.py runserver 0.0.0.0:${PROJ_WEB_PORT}
