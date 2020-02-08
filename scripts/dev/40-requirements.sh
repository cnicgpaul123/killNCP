# 环境变量
. .projrc

# 工作目录
cd ${PROJ_GIT_DIR}

# 合并功能及部署的 requirements.txt
cat scripts/base/requirements.txt >  scripts/requirements.txt
echo "" >> scripts/requirements.txt
cat scripts/host/requirements.txt >> scripts/requirements.txt
