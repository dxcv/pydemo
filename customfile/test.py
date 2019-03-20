# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 8:37
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : test.py
#
# from collections import Iterator
# from collections import Iterable
#
# #迭代器对象
# class OwnIteror( Iterator ):
#      def __init__(self , arrs ):
#           self.index = 0
#           self.arrs = arrs
#      def  next(self):
#           if self.index > len( self.arrs ) - 1:
#               raise StopIteration
#           else:
#               self.index +=1
#               return self.arrs[ self.index - 1 ]
#
# #可迭代对象
# class OwnIterable( Iterable ):
#       def __init__(self ,  arrs ):
#           self.arrs = arrs
#       def __iter__(self):
#           return OwnIteror( self.arrs )
#
# for item in OwnIterable( [ 1,2,3,4,4,6 ] ):
#       print (item)


#迭代器对象
#可迭代对象 （可迭代对象获取迭代器对象）

#生成器

from collections import Iterator
from collections import Iterable


class MyIterator(Iterator):
    '''迭代器'''

    def __init__(self,it):
        self.index=0
        self.it=it

    def next(self):
        self.index+=1
        if self.index >= len(self.it):
            raise StopIteration
        return self.it[self.index]

class MyIterable(Iterable):
    '''可迭代对象'''
    def __init__(self,it):
        self.it=it

    def __iter__(self):
        return MyIterator(self.it)
        # for val in self.it:
        #     yield val


# opetator functools
# map , filter
# sorted sum min max

def mul(a,b):
    return a*b

from functools import partial , reduce , wraps

from operator import itemgetter , methodcaller , attrgetter




if "__main__" == __name__ :
    # a = partial(mul, 3)
    # print(a(3))

    # gloabl = 3
    # a = mul(3 ,gloabl)
    # print(a)

    # dd = [["abc", "xaz"], ["cbd", "add"], ["xxd", "zd"]]
    # d = sorted(dd, key=itemgetter(1))
    # print(d)

    # fz = itemgetter(1,0)
    #
    # for d in dd :
    #     print(fz(d))
    #     pass

    upper = methodcaller('upper')

    s = 'acdfsfsdfsd'

    print(s.upper())

    pass


