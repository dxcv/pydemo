# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 15:17
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : clpa_redis.py
import redis

pool = redis.ConnectionPool(host='192.168.1.232')
r = redis.Redis(connection_pool=pool)




if "__main__" == __name__ :
    print( r.get("brokerinfo_900020") )