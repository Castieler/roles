#coding:utf-8
from impala.dbapi import connect

# 需要注意的是这里的auth_mechanism必须有，默认是NOSASL，但database不必须，user也不必须
from impala.error import HiveServer2Error  # pip install impyla


class HiveCon():
    def __init__(self):
        self.conn = connect(host='10.20.6.17', port=10000, database='default', auth_mechanism='PLAIN',
                       user='hadoop')
        self.cur = self.conn.cursor()
        # self.cur.execute('ADD jar /usr/local/xywy/apache-hive/TmpJar/elasticsearch-hadoop-2.1.0.Beta3.jar')


if __name__ == '__main__':
    a = HiveCon()
    a.cur.execute("show partitions club.query_detail_temp")
    res = a.cur.fetchall()
    print(res[-1][0])
    # import traceback
    #
    # a.cur.execute('ADD jar /usr/local/xywy/apache-hive/TmpJar/elasticsearch-hadoop-2.1.0.Beta3.jar')
    # try:
    #     a.cur.execute('SHOW CREATE TABLE asdds')
    #     res = a.cur.fetchall()
    #     print(res)
    # except HiveServer2Error as e:
    #     # traceback.print_exc()
    #     print('ss')
    # print(cur.fetchall())


