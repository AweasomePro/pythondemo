#!/bin/bash
set -e
LOGFILE = /var/log/blog.log
# log 路径
LOGDIR = $(dirname $ LOGFILE)
NUM_WORKERS = 1
# 下面有解释
# user/group to run as
USER = root
GROUP = root
# cd to your project dir
cd /home/www/...
# web 的路径
test -d $LOGDIR || mkdri -p $LOGDIR
exec gunicorn -w $NUM_WORKERS -b 0.0.0.0:8000 hotelBooking.wsgi:application --user=$USER --group=$GROUP