# 环境变量
. .projrc

# python 虚拟环境
[ -n "${PROJ_PYTHON_ENV}" ] && [ ! -f "${PROJ_PYTHON}" ] && pyenv virtualenv ${PROJ_PYTHON_VER} ${PROJ_PYTHON_ENV}
