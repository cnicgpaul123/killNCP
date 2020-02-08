# 环境变量
. .projrc

# 工作目录
cd ${PROJ_GIT_DIR}

# 安装 libs 下的子模块
for package in `ls libs`; do
    dir="libs/$package"
    if [ -d "$dir" ]; then
        echo "$dir"
        echo $(cd "$dir"; ${PROJ_PYTHON} setup.py -q develop)
    fi
done
