FROM nginx:latest
MAINTAINER "Tao"

ENV WORKSPACE /etc/nginx

COPY config/nginx.conf ${WORKSPACE}/nginx.conf
COPY config/default.conf ${WORKSPACE}/conf.d/default.conf

WORKDIR ${WORKSPACE}
