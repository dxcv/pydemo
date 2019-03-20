# -*- coding: utf-8 -*-
# @Time    : 2018/12/6 17:20
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : Util.py

class Bean(object):
    pass

def ObjectToDict(obj):
    '''对象转字典'''
    result = {}
    for a in dir(obj):
        if a.startswith('_') or a == 'metadata':
            continue

        v = getattr(obj, a)

        if callable(v): #排除可调用的函数
            continue

        if isinstance(v ,Bean):
            result[a]=ObjectToDict(v)
        else:
            result[a] = v

    return result


class DictObj(object):


    def __init__(self,map):
        self.map = map

    def __setattr__(self, name, value):
        if name == 'map':
             object.__setattr__(self, name, value)
             return
        self.map[name] = value

    def __getattr__(self,name):
        v = self.map[name]
        if isinstance(v,(dict)):
            return DictObj(v)
        if isinstance(v, (list)):
            r = []
            for i in v:
                r.append(DictObj(i))
            return r
        else:
            return self.map[name]

    def __getitem__(self,name):
        return self.map[name]

