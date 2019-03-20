# coding:utf-8

import math
import redis


class RedisNews(object):
    def __init__(self):
        # 如果返回是二进制类似 b'3\xe6\x9c\x885\xe6\x97\xa5\xe...'需要加decode_responses=True
        try:
            self.redis = redis.StrictRedis(host='192.168.1.232',port=6379, encoding='utf-8',decode_responses=True,db=1)
        except Exception as e:
            print('redis connect faild')

    def _news_id(self, int_id):
        ''' 新闻id '''
        return 'news:%d' % int(int_id)

    def _news_type(self, news_type):
        ''' 新闻类型 '''
        return 'news_type:%s' % news_type

    def _news_list_name(self):
        ''' 新闻列表名称 '''
        return 'news'

    def add_news(self, news_obj):
        ''' 新增新闻数据 '''

        # 获取到新闻的id
        int_id = int(self.redis.incr('news_id'))
        # 　拼接新闻数据Hash key(news:2)
        news_id = self._news_id(int_id)

        # 存储新闻数据(hash)
        rest = self.redis.hmset(news_id, news_obj)

        # 存储新闻的id list
        self.redis.lpush(self._news_list_name(), int(int_id))

        # 存储新闻的类别-新闻id(set)
        news_type = self._news_type(news_obj['news_type'])
        self.redis.sadd(news_type, int_id)
        return rest