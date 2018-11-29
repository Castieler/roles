#!/bin/bash


CWD=`pwd`
echo $CWD

PIDFILE=$CWD/python_server.pid


case "$1" in

  start)
    nohup /data/hadoop/apps/test.admin.dm.xywy.com/venv1/bin/uwsgi uwsgi.ini >nohup.log 2>&1 &
    nohup /data/hadoop/apps/test.admin.dm.xywy.com/venv1/bin/python manage.py celery worker -c 1 --loglevel=info >celery.log 2>&1 &
    echo $! >> $PIDFILE
    nohup /data/hadoop/apps/test.admin.dm.xywy.com/venv1/bin/python manage.py celery flower >flower.log 2>&1 &
    echo $! >> $PIDFILE
    ;;

  stop)
    kill -9 `cat $PIDFILE`
    rm -rf $PIDFILE
    ;;

  restart)
    sh $0 stop
    sleep 1
    sh $0 start
    ;;

  *)
    echo "Options: {start|stop|restart}"
    ;;

esac

exit 0

