#coding:utf-8
from django.shortcuts import render
from lib.handle_upload_file import handle_uploaded_file
from lib.email_of_exception import sendEmail
from upload_file.task import linux_shell
# Create your views here.
def handle_file(request):
    if request.method == 'GET':
        return render(request, 'upload_file/upload.html')
    elif request.method == 'POST':
        print(request.FILES)
        if 'file' in request.FILES:
            excel_name = handle_uploaded_file(request.FILES['file'])
            if 'xlsx' not in excel_name:
                sendEmail('上传文件出错,不是Excel格式', content=excel_name)
                return render(request, 'upload_file/upload.html', {'info': '上传文件出错,不是Excel格式'})

            linux_shell.delay(excel_name)
            return render(request, 'upload_file/upload.html',{'info':'上传成功'})
        else:
            return render(request, 'upload_file/upload.html',{'info':'请添加Excel文件'})

