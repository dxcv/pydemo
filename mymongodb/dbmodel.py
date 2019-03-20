# -*- coding: utf-8 -*-
# @Time    : 2018/12/6 16:55
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : dbmodel.py

from mymongodb.Util import Bean


class Tcache(Bean):
    __slots__ = ('cache_name','url','createtime','runtime',)

    def __init__(self,cache_name=None,url=None,createtime=None,runtime=None):
        # 缓存名称
        self.cache_name = cache_name
        # url
        self.url = url
        # 创建时间
        self.createtime = createtime
        # 运行时间 cron 表达式
        self.runtime = runtime

    def __str__(self):
        return "cache_name:%s;url:%s;createtime:%s;runtime:%s" % (self.cache_name,self.url,self.createtime,self.runtime)



# t = Tcache(cache_name="粗",url="http://www.baidu.com",createtime=datetime.now(),runtime="XXXX")
# # print(ObjectToDict(t))