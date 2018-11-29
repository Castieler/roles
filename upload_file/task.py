import os
import time
from upload_file import models
from celery import task
from subprocess import call
from lib.email_of_exception import sendEmail as exception_sendEmail
from lib.send_email import sendEmail as work_email
from lib.handle_excel import read_excel
from lib.redis_con import redis_conn


@task
def linux_shell(excel_name):
    _dict = read_excel(excel_name)
    print('生成txt文件')
    date_str_list = _dict['date_list']
    print('开始执行脚本')
    exception_sendEmail('开始执行脚本', '开始执行脚本')
    for date_str in date_str_list:
        call("/bin/bash /data/git/hadoop_mining/data_mining/code/sh_python/guantie_everyday/crawl_for_daily_guantie.sh " + date_str + " 1 > crawl_for_daily_guantie.sh.log ", shell=True)
        # call(
        #     "/bin/bash /data/git/hadoop_mining/data_mining/code/sh_python/guantie_everyday/test.sh " + date_str + " 1 > crawl_for_daily_guantie.sh.log 2>&1",
        #     shell=True)
    print('----------------------------执行结束----------------------------')
    exception_sendEmail('脚本执行结束', '脚本执行结束')
    time_num = 0
    time.sleep(4)
    while 1:
        print('执行循环')
        if time_num == 300:
            exception_sendEmail('crawl_文件读取失败', 'crawl_文件读取失败')
            break
        _str = ''
        flag = True
        for date_str in date_str_list:
            log_path = '/data/logs/tmp_log/guantie_everyday_result/crawl_' + date_str + '.txt'
            if os.path.isfile(log_path):
                res = os.popen('wc -l {log_path}'.format(log_path=log_path)).readlines()
                line_num = res[0].strip().split(' ')[0]
                txt_name = '/data/git/hadoop_mining/data_mining/tempfiles/keywords_detail_{date_str}.txt'
                models.Txt.objects.filter(txt_name=txt_name.format(date_str=date_str)).update(txt_result=line_num)
                if len(date_str_list) == 1:
                    _str += ' 数据量:' + str(line_num) + '\n'
                else:
                    _str += date_str + ' 数据量:' + str(line_num) + '\n'
            else:
                print('此文件不存在：', log_path)
                flag = False
        time_num += 1
        exception_sendEmail('crawl_文件读取完成', _str)
        if flag:
            file_list = _dict['txt']
            for txt_name in file_list:
                res = models.Txt.objects.get(txt_name=txt_name)
                models.File.objects.filter(txt=res).update(flag=True)
            redis_conn.set('DataMingManage-task', 'false')
            # work_email('灌贴项目', '数据已处理并提供，对应数据：\n' + _str)
            break
        else:
            time.sleep(10)
            continue
