#!/usr/bin/env bash

# CNICG 国家平台节点系统自动部署脚本结合 yum
# 请用 maintain(with sudo) 账户运行该脚本
# 确保 目标服务器设置 可以联网
# 创建用户：sudo useradd -G wheel maintain
# 配置密码：sudo passwd maintain

yum_set(){

    sudo yum install wget curl lrzsz -y

    sudo mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
    sudo mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup

    sudo wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.cloud.tencent.com/repo/centos7_base.repo && \
    sudo wget -O /etc/yum.repos.d/epel.repo http://mirrors.cloud.tencent.com/repo/epel-7.repo && \

    sudo yum clean all && \
    sudo yum makecache
    # sudo yum repolist 
}

cnicg_init() {
    [ ! -d /cnicg ] && sudo mkdir /cnicg && sudo chown maintain:maintain /cnicg

    mkdir -p /cnicg/{conf,projs,logs} /cnicg/conf/{nginx,supervisor}/conf.d
}

nginx_install(){

    sudo yum install nginx -y
    # append /etc/nginx/nginx.conf
    # include /cnicg/conf/nginx/conf.d/*.conf

    sudo systemctl enable nginx.service
    sudo systemctl start nginx.service

}

supervisor_install(){

    sudo yum -y install supervisor
    # append /etc/supervisord.conf
    # include /cnicg/conf/supervisor/conf.d/*.conf

    sudo systemctl start supervisord
    sudo systemctl enable supervisord
}

python3_install(){

    mkdir -p ~/.pip
    echo "[global]" > ~/.pip/pip.conf
    echo "cache-dir = /tmp/cache-pip" >> ~/.pip/pip.conf
    echo "index-url = http://mirrors.aliyun.com/pypi/simple/" >> ~/.pip/pip.conf
    echo "trusted-host = mirrors.aliyun.com" >> ~/.pip/pip.conf

    sudo yum -y install python36 python36-devel python36-setuptools

    # install pip3
    curl -fSL https://bootstrap.pypa.io/get-pip.py | sudo python36
    echo "alias sudo='sudo env PATH=\$PATH'" | tee -a ~/.bashrc && \
    sudo pip3 install uwsgi

}

mongodb_install(){

    sudo yum -y install mongodb mongodb-server mongodb-test
    sudo systemctl start mongod
    sudo systemctl enable mongod

}

mariadb_install(){

    sudo yum -y install mariadb mariadb-server
    sudo systemctl start mariadb
    sudo systemctl enable mariadb

    # initialize root password
    # mysql_secure_installation
    # GRANT ALL PRIVILEGES ON `iot`.* TO  iot'@'localhost'
}


nvm_clone() {
    git -c advice.detachedHead=false clone \
        https://github.com/creationix/nvm.git \
        -b v0.33.11 \
        --depth=1 \
        "$1"
}

nvm_install() {

    echo "registry=https://registry.npm.taobao.org" > ~/.npmrc
    NVM_DIR="/cnicg/app/nvm"
    mkdir -p "$NVM_DIR"
    nvm_clone "$NVM_DIR"
    chmod +x "$NVM_DIR/nvm.sh"
    echo "export NVM_DIR=\"$NVM_DIR\"" >> ~/.bash_profile
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm' >> ~/.bash_profile
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion' >> ~/.bash_profile

    # nvm ls-remote --lts | grep -i "latest"
    # nvm install 10
}


yum_set

if [[ $? -ne 0 ]]; then
echo "yum_set 异常，请检查"
exit 120
fi

cnicg_init

if [[ $? -ne 0 ]]; then
echo "cnicg_init 异常，请检查"
exit 120
fi

nginx_install

if [[ $? -ne 0 ]]; then
echo "nginx_install 异常，请检查"
exit 120
fi

supervisor_install

if [[ $? -ne 0 ]]; then
echo "supervisor_install 异常，请检查"
exit 120
fi

python3_install

if [[ $? -ne 0 ]]; then
echo "python3_install 异常，请检查"
exit 120
fi

mongodb_install

if [[ $? -ne 0 ]]; then
echo "mongodb_install 异常，请检查"
exit 120
fi

mariadb_install

if [[ $? -ne 0 ]]; then
echo "mariadb_install 异常，请检查"
exit 120
fi

# nvm_install

# if [[ $? -ne 0 ]]; then
# echo "nvm_install 异常，请检查"
# exit 120
# fi

echo "All of the base app were installed succesfull"
