# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 12:25
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : emailUtil.py

import smtplib
from email.mime.text import MIMEText
from email.header import Header

#发送邮件
sender = '1548006030@qq.com'
#接受邮件
receivers = ['xulianjun@erichfund.com']

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('开心就好', 'plain', 'utf-8')
message['From'] = Header("测试", 'utf-8')  # 发送者
message['To'] = Header("测试", 'utf-8')  # 接收者
message['Subject'] = Header('测试', 'utf-8')

try:
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "1548006030@qq.com"  # 用户名
    mail_pass = "xxx"  # 口令

    # smtpObj = smtplib.SMTP('localhost')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except smtplib.SMTPException as e:
    print(e)
    print ("Error: 无法发送邮件")