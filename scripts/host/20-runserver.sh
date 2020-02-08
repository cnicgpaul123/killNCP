# 环境变量
. .projrc

# 设定工作目录
cd ${PROJ_GIT_DIR}

# 启动服务(uwsgi)
${PROJ_PYTHON_BIN}/uwsgi --ini ${PROJ_GIT_DIR}/scripts/host/uwsgi.ini
