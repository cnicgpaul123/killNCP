# 环境变量
. .projrc

# 设定工作目录
cd ${PROJ_GIT_DIR}

# 通过 command 处理业务数据
# ${PROJ_PYTHON} manage.py COMMAND ...
# ...
# ${PROJ_PYTHON} manage.py COMMAND ...

# celery 任务及配置
# ${PROJ_PYTHON} manage.py celery_beat load
