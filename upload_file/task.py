import os
import time

from celery import task
from subprocess import call
from lib.send_email import sendEmail
from lib.handle_excel import read_excel


@task
def linux_shell(excel_name):
    # time.sleep(40)
    # sendEmail('灌贴项目', 'test')
    _dict = read_excel(excel_name)
    print('生成txt文件')
    data_str_list = _dict['date_list']
    print('开始执行脚本')
    for data_str in data_str_list:
        # call("/bin/bash /data/git/hadoop_mining/data_mining/code/sh_python/guantie_everyday/crawl_for_daily_guantie.sh "+ data_str +" 1 > crawl_for_daily_guantie.sh.log 2>&1", shell=True)
        call(
            "/bin/bash /data/git/hadoop_mining/data_mining/code/sh_python/guantie_everyday/test.sh " + data_str + " 1 > crawl_for_daily_guantie.sh.log 2>&1",
            shell=True)
    print('----------------------------执行结束----------------------------')
    time_num = 0
    while 1:
        print('执行循环')
        if time_num == 300:
            sendEmail('crawl_文件读取失败', 'crawl_文件读取失败')
            break
        _str = ''
        flag = True
        for data_str in data_str_list:
            log_path = '/data/logs/tmp_log/guantie_everyday_result/crawl_' + data_str +'.txt'
            if os.path.isfile(log_path):
                res = os.popen('wc -l {log_path}'.format(log_path=log_path)).readlines()
                line_num = res[0].strip().split(' ')[0]
                if len(data_str_list) == 1:
                    _str += ' 数据量:' + str(line_num) + '\n'
                else:
                    _str += data_str + ' 数据量:'+str(line_num) + '\n'
            else:
                print('此文件不存在：',log_path)
                flag = False
        time_num += 1
        if flag:
            sendEmail('灌贴项目', '数据已处理并提供，对应数据：\n'+ _str )
            break
        else:
            time.sleep(30)
            continue
