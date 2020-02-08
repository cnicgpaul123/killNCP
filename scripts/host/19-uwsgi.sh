. .projrc && cat <<EOF > scripts/host/uwsgi.ini
[uwsgi]
virtualenv = $(realpath ${PROJ_PYTHON_BIN}/..)
# pythonpath = ${PROJ_PYTHON}
chdir = ${PROJ_GIT_DIR}
wsgi-file = proj/wsgi.py
socket = :${PROJ_WEB_PORT}
; spawn the master & processes
master = true
processes = 4
logto = ${PROJ_LOG_DIR}/uwsgi-django.log
EOF