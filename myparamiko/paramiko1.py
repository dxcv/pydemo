
# encoding : utf-8

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.1.233", 22, "root", "erichfund_2017")
stdin, stdout, stderr =ssh.exec_command('cd /cljj/apps/60.API-CHANNEL/;pwd')
stdin1, stdout1, stderr1 =ssh.exec_command('ls -l')
print(stdout1.readlines())
ssh.close()

