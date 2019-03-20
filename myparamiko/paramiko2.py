# encoding:utf-8

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.1.233', username='root', password='erichfund_2017')
# 务必要加上get_pty=True,否则执行命令会没有权限
stdin, stdout, stderr = ssh.exec_command('ps -ef|grep java', get_pty=True)
# result = stdout.read()
# 循环发送消息给前端页面
while True:
    nextline = stdout.readline().strip()  # 读取脚本输出内容
    print(nextline.strip())
    # 判断消息为空时,退出循环
    if not nextline:
        break

ssh.close()  # 关闭ssh连接