# from subprocess import call
# # a = call("echo Hello World", shell=True)
# # a = call(['pip','-V'], shell=False)
# # print(a)
# cmd = ['ls', '-l']
# ret = call(cmd,stdout=True)
# print(ret)
import re
import subprocess
#
# s = '/data/git/hadoop_mining/data_mining/tempfiles/keywords_detail_2018-12-16.txt'
#
# rex = re.compile(r'\d{1,4}-\d{1,2}-\d{1,2}')
# a = re.search(rex,s).group()
# print(a)
#
# def get_status_output(*args, **kwargs):
#     p = subprocess.Popen(*args, **kwargs)
#     stdout, stderr = p.communicate()
#     return p.returncode, stdout, stderr

# print(get_status_output('pip -V'.split(' ')))

# import os
# a = os.system('ls')

# import os
# a = os.popen('wc -l handle_excel.py').readlines()
# print(a[0].strip().split(' ')[0])

from subprocess import call

call("/bin/bash /data/git/hadoop_mining/data_mining/code/sh_python/guantie_everyday/test.sh " + '2018-12-18' + " 1 > crawl_for_daily_guantie.sh.log ", shell=True)