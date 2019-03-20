# -*- coding: utf-8 -*-
# @Time    : 2019/1/14 10:58
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : connect.py

import ssh
# 新建一个ssh客户端对象
myclient = ssh.SSHClient()
# 设置成默认自动接受密钥
myclient.set_missing_host_key_policy(ssh.AutoAddPolicy())
# 连接远程主机
myclient.connect("192.168.1.233", port=22, username="root", password="erichfund_2017")
# 在远程机执行shell命令
stdin, stdout, stderr = myclient.exec_command("ls -l")
# 读返回结果
print (stdout.read() )
# 在远程机执行python脚本命令
# stdin, stdout, stderr = myclient.exec_command("python /home/test.py")


stdin, stdout, stderr = myclient.exec_command("pwd")
# 读返回结果
print (stdout.read() )
# 新建 sftp session
sftp = myclient.open_sftp()
# 创建目录
# sftp.mkdir('abc')
# 从远程主机下载文件，如果失败， 这个可能会抛出异常。
sftp.get('/root/1', 'C:/Users/JS-007/PycharmProjects')
# 上传文件到远程主机，也可能会抛出异常
# sftp.put('/home/test.sh', 'test.sh')