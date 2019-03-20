# -*- coding: utf-8 -*-
# @Time    : 2019/1/2 13:05
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : __init__.py.py


import os

#切换到指定目录 C:/Users/JS-007/Desktop/filetestdemo
#在改目录下面建一个文件夹
#在建好的文件夹下面创建test.txt  文件，写上hallo world

# os.chdir("C:/Users/JS-007/Desktop/filetestdemo") #切换目录
# if not os.path.exists("test"):
#     os.mkdir("test") #创建目录
# os.chdir("test") #切换目录
# with open("test.txt",'w') as f: #传教文本，写人内容
#     f.write("hallo world")


#删除C:/Users/JS-007/Desktop/filetestdemo/test 目录下面的test.txt ,新建一个test1.txt
# os.chdir("C:/Users/JS-007/Desktop/filetestdemo") #切换目录
# os.chdir("test")
# # print(os.getcwd())
# if os.path.exists("test.txt"):
#     os.remove("test.txt")
# with open("test1.txt",'w') as f:
#     f.write("20190102")

#获取filetestdemo当前目录下面的文件/文件夹列表
os.chdir("C:/Users/JS-007/Desktop/filetestdemo") #切换目录
# ll=os.listdir(os.path.abspath("."))
# for f in ll:
#     if os.path.isfile(f):
#         print( os.path.basename(f)+ "-文件" + "; 大小："+ str(os.path.getsize(f)))
#     elif os.path.isdir(f):
#         print(os.path.basename(f)+"-目录"+ "; 大小："+ str(os.path.getsize(f)))

#删除目录下所有文件夹
import os
import shutil
os.chdir("C:/Users/JS-007/Desktop/filetestdemo") #切换目录
ll=os.listdir(os.path.abspath("."))
for f in ll:
    if os.path.isdir(f):
        print(os.path.basename(f))
        print(os.path.getsize(f))
        if os.path.getsize(f) == 0:#不能通过文件大小判断文件夹是否为空文件夹
            os.rmdir(os.path.basename(f)) #清空空文件夹
            # shutil.rmtree(os.path.basename(f)) #递归删除文件夹


#修改文件名称
# os.chdir("C:/Users/JS-007/Desktop/filetestdemo") #切换目录
# if not os.path.exists("test111"):
#     os.rename("test","test111")