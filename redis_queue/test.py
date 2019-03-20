
# -*- coding:utf-8  -*-

import redis

my_redis= redis.StrictRedis(host='192.168.1.232',port=6379, encoding='utf-8',decode_responses=True,db=1)


