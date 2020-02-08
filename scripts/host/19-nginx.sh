. .projrc && cat <<EOF > scripts/host/nginx.conf
server {
  listen 80;
  server_name ${PROJ_DOMAIN};
  access_log ${PROJ_LOG_DIR}/access.log;
  error_log  ${PROJ_LOG_DIR}/error.log;
  location ~ ^/api/[^/]+\.js(on)?$ {
    root ${STATIC_ROOT}/ssr/;
    expires 1d;
    include /cnicg/resources.git/nginx/gzip.conf;
  }
  location ~ ^/(admin|api|views)/ {
    uwsgi_pass 127.0.0.1:${PROJ_WEB_PORT};
    include uwsgi_params;
  }
  location ${STATIC_URL} {
    alias ${STATIC_ROOT}/;
    expires 5d;
    include /cnicg/resources.git/nginx/gzip.conf;
  }
  location ${MEDIA_URL} {
    alias ${MEDIA_ROOT}/;
    expires 5d;
    include /cnicg/resources.git/nginx/gzip.conf;
  }
  #location /admin/ {
    #alias ${ADMIN_WWW_ROOT}/;
    #index index.html index.htm;
    #expires 5d;
    #include /cnicg/resources.git/nginx/gzip.conf;
  #}
  location / {
    root ${PUB_WWW_ROOT}/;
    expires 5d;
    include /cnicg/resources.git/nginx/gzip.conf;
  }
  #location / {
    #proxy_pass http://127.0.0.1:${NUXT_WEB_PORT};
    #proxy_set_header Host \$host;
    #proxy_set_header X-Real-IP \$remote_addr;
    #proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    #add_header Content-Security-Policy "img-src 'self' data: *.clouddn.com;*.cniotroot.cn;";
    #add_header Content-Security-Policy "img-src *";
  #}
  include /cnicg/resources.git/nginx/favicon.conf;
  include /cnicg/resources.git/nginx/robots.conf;
  include /cnicg/resources.git/nginx/ssl.conf;
}
EOF