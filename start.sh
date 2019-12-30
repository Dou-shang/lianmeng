#!/bin/bash
cd /root/tiktok-shop/
uwsgi --ini ./uwsgi.ini &
nginx -c /etc/nginx/nginx.conf
