import redis
#test_port =  8002
#test_ip = 127.0.0.1

redis_config = {
    # "host": "rm6934i.redis.service.op.xywy.com",
    # "port": 6934
    "host":"10.30.1.23",
    "port":6379,
}
# redis连接对象
redis_conn = redis.Redis(**redis_config)
if __name__ == '__main__':
    redis_conn.set('DataMingManage-task', 'false')