from impala.dbapi import connect

# 需要注意的是这里的auth_mechanism必须有，默认是NOSASL，但database不必须，user也不必须
from impala.error import HiveServer2Error

conn = connect(host='10.20.6.17', port=10000, database='default', auth_mechanism='PLAIN',
               user='hadoop')
cur = conn.cursor()
cur.execute('ADD jar /usr/local/xywy/apache-hive/TmpJar/elasticsearch-hadoop-2.1.0.Beta3.jar')
if __name__ == '__main__':
    import traceback
    cur.execute('ADD jar /usr/local/xywy/apache-hive/TmpJar/elasticsearch-hadoop-2.1.0.Beta3.jar')
    try:
        cur.execute('SHOW CREATE TABLE asdds')
        res = cur.fetchall()
        print(res)
    except HiveServer2Error as e:
        # traceback.print_exc()
        print('ss')
    # print(cur.fetchall())


