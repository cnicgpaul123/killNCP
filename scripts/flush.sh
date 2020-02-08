. .projrc

# 创建 pyenv 虚拟环境；如无需 pyenv，则注释
echo "##### check python / pyenv ..."
. scripts/host/02-pyenv.sh
[[ $@ =~ "--to-pyenv" ]] && exit 0

# 安装依赖
[[ $@ =~ "--no-pip" ]] && exit 0
echo "##### check libraries ..."
. scripts/host/02-pip.sh
. scripts/base/02-pip.sh
. scripts/dev/40-submodules.sh
[[ $@ =~ "--to-pip" ]] && exit 0

# 更新项目配置
[[ $@ =~ "--no-environ" ]] && exit 0
echo "##### update environ ..."
. scripts/base/03-environ.sh
[[ $@ =~ "--to-environ" ]] && exit 0

# 更新数据
[[ $@ =~ "--no-prepare" ]] && exit 0
echo "##### prepare data ..."
. scripts/base/10-prepare.sh
[[ $@ =~ "--to-prepare" ]] && exit 0

# 系统服务配置
[[ $@ =~ "--no-servconf" ]] && exit 0
echo "##### update uwsgi & supervisor & nginx configuration"
. scripts/host/19-uwsgi.sh
. scripts/host/19-supervisor.sh
. scripts/host/19-nginx.sh
# scripts/host/19-nuxt.sh
[[ $@ =~ "--to-servconf" ]] && exit 0
