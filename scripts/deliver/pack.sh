# 项目Git仓库
PROJ_GIT_URL=git@git.dev.cnicg.cn:deliver/REPO.git
# 项目Git版本分支
PROJ_GIT_BRANCH=master
# 打包文件
PROJ_NAME=PRODUCT

git clone -q --recursive ${PROJ_GIT_URL} -b ${PROJ_GIT_BRANCH} ${PROJ_NAME}

cd ${PROJ_NAME}
rm -rf .git*
rm -rf scripts/deliver/pack*
rm -rf scripts/allinone.sh
rm -rf scripts/host/{00,01}-git*.sh

sed -i -e 1c"PROJ_GIT_DIR=/cnicg/projs/PRODUCT" scripts/base/environ.sample.rc
sed -i "s/PROJ_PYTHON_ENV=.*/PROJ_PYTHON_ENV=/" scripts/base/environ.sample.rc
sed -i "s/PROJ_PYTHON_BIN=.*/PROJ_PYTHON_BIN=\/usr\/local\/bin/" scripts/base/environ.sample.rc
sed -i "s/PROJ_PYTHON=.*/PROJ_PYTHON=\/usr\/bin\/python36/" scripts/base/environ.sample.rc

sed -i "s/STATIC_ROOT=.*/STATIC_ROOT=\${PROJ_GIT_DIR}\/web/" scripts/base/environ.sample.rc
sed -i "s/MEDIA_ROOT=.*/MEDIA_ROOT=\${PROJ_GIT_DIR}\/media/" scripts/base/environ.sample.rc
sed -i "s/PROJ_LOG_DIR=.*/PROJ_LOG_DIR=\/cnicg\/logs\/PRODUCT/" scripts/base/environ.sample.rc

sed -i "s/; \${PROJ_PYTHON}/; sudo \${PROJ_PYTHON}/" scripts/dev/40-submodules.sh
sed -i "s/^\${PROJ_PIP}/sudo \${PROJ_PIP}/" scripts/base/02-pip.sh
sed -i "s/^\${PROJ_PIP}/sudo \${PROJ_PIP}/" scripts/dev/02-pip.sh
sed -i "s/^\${PROJ_PIP}/sudo \${PROJ_PIP}/" scripts/host/02-pip.sh
sed -i "s/http\:\/\/git\.dev\.cnicg\.cn\/cnicg\/apps\/django_celery_management/https\:\/\/github.com\/princeofdatamining\/django_celery_management/" scripts/requirements.txt
sed -i "s/http\:\/\/git\.dev\.cnicg\.cn\/cnicg\/apps\/django_celery_management/https\:\/\/github.com\/princeofdatamining\/django_celery_management/" scripts/base/requirements.txt

sed -i "s/include \/cnicg\/resources.git\/nginx\/gzip\.conf/#include \/path\/to\/gzip\.conf/" scripts/host/19-nginx.sh
sed -i "s/include \/cnicg\/resources.git\/nginx\/favicon\.conf/#include \/path\/to\/favicon\.conf/" scripts/host/19-nginx.sh
sed -i "s/include \/cnicg\/resources.git\/nginx\/robots\.conf/#include \/path\/to\/robots\.conf/" scripts/host/19-nginx.sh
sed -i "s/include \/cnicg\/resources.git\/nginx\/ssl\.conf/#include \/path\/to\/ssl\.conf/" scripts/host/19-nginx.sh

sed -i "s/^virtualenv/# virtualenv/" scripts/host/19-uwsgi.sh
sed -i "s/^# pythonpath/pythonpath/" scripts/host/19-uwsgi.sh

cd ..
tar -czf ${PROJ_NAME}.tar.gz ${PROJ_NAME}
