#!/bin/bash
# 一键部署脚本
# example: 无参数

###### .gitrc ######
# 项目 Git 仓库(本机需要公钥并在 git 服务中登记)
PROJ_GIT_URL=git@git.dev.cnicg.cn:USER_OR_GROUP/PROJECT.git
# 项目 Git 版本分支
PROJ_GIT_BRANCH=master
# 项目 Git 目录(目录、权限依赖于运维或开发规范，不在应用中涉及)
PROJ_GIT_DIR=/cnicg/projs/GROUP/PROJ/src

###### .projrc ######
# 项目的环境配置文件
ENVIRON_RC=/cnicg/environs.git/GROUP/PROJ.rc
# 部署环境，如"prod", "testing" # 可自行定义（需对应环境配置仓库中的分支名）
ENVIRON_NAME=prod
# 环境配置仓库，可自行管理，但分支名、文件名需符合前两项中的指定
ENVIRON_GIT=git@git.dev.cnicg.cn:USER_OR_GROUP/deploy-environ.git

anynowtime="date +'%Y-%m-%d %H:%M:%S'"
NOW="echo [\`$anynowtime\`][PID:$$]"

##### 可在脚本开始运行时调用，打印当时的时间戳及PID。
function job_start
{
    echo "`eval $NOW` job_start"
}

##### 可在脚本执行成功的逻辑分支处调用，打印当时的时间戳及PID。 
function job_success
{
    MSG="$*"
    echo "`eval $NOW` job_success:[$MSG]"
    exit 0
}

##### 可在脚本执行失败的逻辑分支处调用，打印当时的时间戳及PID。
function job_fail
{
    MSG="$*"
    echo "`eval $NOW` job_fail:[$MSG]"
    exit 1
}

job_start

###### 可在此处开始编写您的脚本逻辑代码
###### 作业平台中执行脚本成功和失败的标准只取决于脚本最后一条执行语句的返回值
###### 如果返回值为0，则认为此脚本执行成功，如果非0，则认为脚本执行失败

# 克隆/更新 git
echo "##### Update / clone from git ..."
if [ ! -d ${PROJ_GIT_DIR} ]; then
    mkdir -p ${PROJ_GIT_DIR} && git clone --recursive -b ${PROJ_GIT_BRANCH} ${PROJ_GIT_URL} ${PROJ_GIT_DIR}
    cd ${PROJ_GIT_DIR}
else
    cd ${PROJ_GIT_DIR}
    git fetch && git checkout ${PROJ_GIT_BRANCH} && git pull && git submodule init && git submodule update
fi
echo "##### pwd: $(pwd)"

###### .gitrc ######
echo "PROJ_GIT_URL=\"${PROJ_GIT_URL}\"" > .gitrc
echo "PROJ_GIT_BRANCH=\"${PROJ_GIT_BRANCH}\"" >> .gitrc
echo "PROJ_GIT_DIR=\"${PROJ_GIT_DIR}\"" >> .gitrc


# 【环境】项目配置
if [ ! -d /cnicg/environs.git ]; then
    git clone -b ${ENVIRON_NAME} ${ENVIRON_GIT} /cnicg/environs.git
else
    echo $(cd /cnicg/environs.git; git fetch; git checkout ${ENVIRON_NAME}; git pull) 
fi
# 也可以采用其他方式：http/scp 等等


# 【通用】模板及资源
echo "##### update / clone resources & templates ..."
if [ ! -d /cnicg/resources.git ]; then
    git clone -b v1 git@git.dev.cnicg.cn:devops/resources.git /cnicg/resources.git
else
    echo $(cd /cnicg/resources.git; git pull) 
fi


# 应用项目配置
source "${ENVIRON_RC}"
###### .projrc ######
cat "${ENVIRON_RC}" > .projrc
! command grep -qc '. .gitrc' .projrc && echo "append .gitrc" && sed -i -e 1c". .gitrc # 引入 git 配置项" .projrc
###### .projrc ######
. scripts/flush.sh


echo "##### update & reload supervisor ..."
SUPERVISOR_CONF=/cnicg/conf/supervisor/supervisord.conf
[ ! -f ${SUPERVISOR_CONF} ] && job_fail "Not found: ${SUPERVISOR_CONF}"
SUPERVISOR_CONF_D="/cnicg/conf/supervisor/conf.d"
rm -f ${SUPERVISOR_CONF_D}/${GROUP_CODENAME}__${PROJ_CODENAME}.conf
ln -s ${PROJ_GIT_DIR}/scripts/host/supervisor.conf ${SUPERVISOR_CONF_D}/${GROUP_CODENAME}__${PROJ_CODENAME}.conf
if [ 0 -eq `ps aux | grep supervisord | grep -v grep | wc -l` ]; then
    echo "supervisor: run ..." && supervisord
elif [ 0 -eq `supervisorctl status | grep ${PROJ_CODENAME} | wc -l` ]; then
    echo "supervisor: update ..." && supervisorctl update
else
    echo "supervisor: update ..." && supervisorctl update
    echo "supervisor: restart ..." && supervisorctl restart "${PROJ_CODENAME}:*"
fi


echo "##### update & reload nginx ..."
NGINX_CONF=/cnicg/conf/nginx/nginx.conf
[ ! -f ${NGINX_CONF} ] && job_fail "Not found: ${NGINX_CONF}"
NGINX_CONF_D="/cnicg/conf/nginx/conf.d"
rm -f ${NGINX_CONF_D}/${GROUP_CODENAME}__${PROJ_CODENAME}.conf
ln -s ${PROJ_GIT_DIR}/scripts/host/nginx.conf ${NGINX_CONF_D}/${GROUP_CODENAME}__${PROJ_CODENAME}.conf
if [ 0 -eq `ps aux | grep nginx | grep -v grep | wc -l` ]; then
    echo "nginx: run ..." && nginx
else
    echo "nginx: reload ..." && nginx -s reload
fi

job_success
