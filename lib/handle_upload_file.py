import os
import time
from django.conf import settings

def handle_uploaded_file(f):
    file_name = ""
    try:
        path = 'upload_file/data'
        file_name = os.path.join(path,time.strftime('%Y_%m_%d__') + f.name)
        print('file_name',file_name)
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as e:
        print(e)
    return os.path.abspath(file_name)