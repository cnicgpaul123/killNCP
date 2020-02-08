. .gitrc # 引入环境变量

# 【创建】项目目录(目录、权限依赖于运维或开发规范，不在应用中涉及)
mkdir -p ${PROJ_GIT_DIR}

# 【创建】克隆指定版本(请在新的环境上操作，不考虑项目是否存在、是否统一项目)
git clone --recursive -b ${PROJ_GIT_BRANCH} ${PROJ_GIT_URL} ${PROJ_GIT_DIR}

# .gitrc 移到项目目录下
mv .gitrc ${PROJ_GIT_DIR}/
