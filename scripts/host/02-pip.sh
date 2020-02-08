# 环境变量
. .projrc

# 工作目录
cd ${PROJ_GIT_DIR}

# 第三方依赖
${PROJ_PIP} install -q -r scripts/host/requirements.txt
