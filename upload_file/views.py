#coding:utf-8
from django.shortcuts import render
from lib.handle_upload_file import handle_uploaded_file
from lib.email_of_exception import sendEmail as exception_sendEmail
from upload_file.task import linux_shell
from lib.last_request_url import save_request_url
from lib.redis_con import redis_conn

@save_request_url
def handle_file(request, *args):
    if request.method == 'GET':
        task = redis_conn.get('DataMingManage-task')
        if not task:
            task = 'false'
        return render(request, 'upload_file/upload.html', {'task': task.decode('utf-8') if type(task) == bytes else task})
    elif request.method == 'POST':
        if 'file' in request.FILES:
            file_name = request.FILES['file'].name
            if 'xlsx' not in file_name:
                exception_sendEmail('上传文件出错,不是Excel格式', content=file_name)
                return render(request, 'upload_file/upload.html', {'info': '上传文件出错,不是Excel格式'})
            excel_name = handle_uploaded_file(request.FILES['file'])
            redis_conn.set('DataMingManage-task', 'true')
            task = redis_conn.get('DataMingManage-task')
            if not task:
                task = 'false'
            linux_shell.delay(excel_name)
            return render(request, 'upload_file/upload.html', {'info':'上传成功','task': task.decode('utf-8') if type(task) == bytes else task})
        else:
            task = redis_conn.get('DataMingManage-task')
            if not task:
                task = 'false'
            return render(request, 'upload_file/upload.html', {'info':'请添加Excel文件','task':task.decode('utf-8') if type(task) == bytes else task})

