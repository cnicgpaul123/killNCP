# 环境变量
. .projrc

# 工作目录
cd ${PROJ_GIT_DIR}

lint() {
    for folder in `ls "$1"`; do
        if [ -f "$1/$folder/__init__.py" ]; then
            echo "pylint $1/$folder ..."
            ${PROJ_PYTHON_BIN}/pylint "$1/$folder"
        fi
    done
}

# 处理所有子模块
for package in `ls libs`; do
    dir="libs/$package"
    if [ -d "$dir" ]; then
        lint "$dir"
    fi
done
