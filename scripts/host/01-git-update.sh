. .gitrc # 引入环境变量

# 设定工作目录
cd ${PROJ_GIT_DIR}

# 【更新】指定版本
git fetch
git checkout ${PROJ_GIT_BRANCH}
git pull

# 【更新】子模块
git submodule init
git submodule update
