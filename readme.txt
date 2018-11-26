which python3
/data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/python

which pip3
/data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/pip3

部署到这个目录，代码和日志在一起就可以
/data/hadoop/apps/test.admin.dm.xywy.com

# nohup /data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/python manage.py runserver 0.0.0.0:8100 >nohup.log 2>&1 &

# 启动celery（执行异步任务）
安装： /data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/pip3 install celery
         /data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/pip3 install celery django-celery
 启动  nohup /data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/python manage.py celery worker -c 4 --loglevel=info >celery.log 2>&1 &

 # 异步任务界面
 安装：/data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/pip3 install flower
 启动：nohup /data/hadoop/apps/test.admin.dm.xywy.com/version3/venv1/bin/python manage.py celery flower >flower.log 2>&1 &
 http://10.20.6.17:5555