# -*- coding:utf-8 -*-

from redis_queue import RedisQueue
import time

q = RedisQueue('rq')  # 新建队列名为rq
for i in ["a","b","c","d","e","f"]:
    q.put(i)
    print ( "input.py: data {} enqueue {}".format(i, time.strftime("%c")) )
    time.sleep(1)