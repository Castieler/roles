# -*- coding: utf-8 -*-
import os
import platform
from upload_file import models
from .email_of_exception import sendEmail
import xlrd
import xlwt
import datetime
import traceback
from .python_hive import HiveCon
hive_con = HiveCon()
if platform.system() == 'Darwin':
    txtpath = os.path.dirname(__file__)
else:
    txtpath = '/data/git/hadoop_mining/data_mining/tempfiles'

def read_excel(_path):
    # 打开文件
    workbook = xlrd.open_workbook(_path)
    try:
        hive_con.cur.execute("show partitions club.query_detail_temp")
        res = hive_con.cur.fetchall()
        startdate = datetime.datetime.strptime(res[-1][0].replace('time=', ''), "%Y-%m-%d")
        tomorrow = startdate + datetime.timedelta(days=1)
    except Exception as e:
        exception = traceback.format_exc()
        traceback.print_exc()
        sendEmail(title='hive服务挂了', content=exception)
    file_list = []
    date_list = []
    for sheet_name in workbook.sheet_names():
        sheet2 = workbook.sheet_by_name(sheet_name)
        # 保存第一列数据
        cols = sheet2.col_values(0)
        date_list.append(str(tomorrow.date()))
        file_1 = os.path.join(txtpath, 'keywords_' + str(tomorrow.date()) +'.txt')
        f = open(file_1,'w')
        for each_line in cols[1:]:
            f.write(each_line.strip() + '\n')
        f.close()
        # 保存所有数据
        file_2 = os.path.join(txtpath, 'keywords_detail_' + str(tomorrow.date()) +'.txt')


        file_list.append(file_2)
        t = open(file_2, 'w')
        for row in range(1, sheet2.nrows):
            string = ''
            for col in range(4):
                if col == 3:
                    string = string + str(sheet2.cell(row, col).value)
                elif col == 1 or col == 2:
                    string = string + str(int(float(sheet2.cell(row, col).value))) + '\t'
                else:
                    string = string + str(sheet2.cell(row, col).value) + '\t'
            t.write(string+'\n')
        t.close()
        tomorrow = tomorrow + datetime.timedelta(days=1)

    for txt_name in file_list:
        txt_queryset = models.Txt.objects.filter(txt_name=txt_name)
        if not txt_queryset:
            models.Txt.objects.create(txt_name=txt_name)
        res = models.Txt.objects.get(txt_name=txt_name)
        file_queryset = models.File.objects.filter(txt=res)
        if not file_queryset:
            models.File.objects.create(excel_name=_path, sheet_num=len(file_list), txt=res)



    return {'excel': _path, 'txt': file_list,'date_list': date_list}
if __name__ == '__main__':
    read_excel('a.xlsx')