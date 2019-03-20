# -*- coding:utf-8 -*-


'''

raise           必须的，没有就抛出异常
if 不满足 :
    raise Exception("xxxxxxx")
继续 给默认值    可以提前给，正常再赋值覆盖掉默认的
a = default
if 存在 ：
    a = 1

if
分支
校验 （break,contiune）

'''

# def foo():
#     data = []
#     s = []
#     if not data :
#         raise Exception()
#     if not s :
#         raise Exception()
#
#     if data :
#         if s :
#             pass
#
#
#     return None


import numpy as np
# 正态生成4行5列的二维数组
# arr = np.random.normal(1.75, 0.1, (4, 5))
# print(arr)
# 截取第1至2行的第2至3列(从第0行算起)
# after_arr = arr[1:3, 2:4]
# print(after_arr)



# stus_score = np.array([[80, 88], [82, 81], [84, 75], [86, 83], [75, 81]])
# # 平时成绩占40% 期末成绩占60%, 计算结果
# q = np.array([[0.4], [0.6]])
# result = np.dot(stus_score, q)
# print("最终结果为:")
# print(result)

# 多于一个维度
# import numpy as np
# a = np.array([3,4])
# print (a)
import os
csv_dir = os.path.dirname(os.path.abspath(__file__))

csvfifle = "%s/%s" % (csv_dir,'found.csv')

print(csvfifle)
