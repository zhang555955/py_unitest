#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : send_Emain.py
# @Author: 橘子
# @Date  : 2021/1/12
# @Desc  : execise

import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

#定义发件人和收件人
# mail_host="smtp.qq.com"  #设置服务器
# mail_user="******"    #用户名
# mail_pass="******"   #口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
# sender = '******'
mail_host = "smtp.qq.com"  #设置服务器
mail_from = "******"
mail_password = "******"
mail_to = ["******"]

def email_content():
    #邮件主题
    message = MIMEMultipart()
    message['From'] = Header(u"姓名" + "<" + mail_from + ">", 'utf-8')
    message['To'] = ";".join(mail_to)
    message['Subject'] = Header(u"接口自动化测试报告", 'utf-8')

    #邮件内容
    emailContent1 = MIMEText('这是测试报告，详情查看附件', 'plain')
    message.attach(emailContent1)

    #获取最新的html报告
    result_dir = "G:/py_unitest/testreport"
    #result_dir = os.path.join(os.getcwd(),'report/')
    lists = os.listdir(result_dir)
    print("最新的文件为：" + lists[-2])
    file = os.path.join(result_dir, lists[-2])

    #构造图片链接
    sendimagefile = open(r'G:/phototest/1.jpg', 'rb').read()
    image = MIMEImage(sendimagefile)
    image.add_header('Content-ID', '<image1>')
    image["Content-Dispositon"] = 'attachment; filename="1.jpg"'
    message.attach(image)



    #邮件内容2：report.html中内容
    emailContent2 = MIMEText(open(file, 'rb').read(), 'html', 'utf-8')
    message.attach(emailContent2)

    #添加邮件附件
    enclosure1 = MIMEText(open(file, 'rb').read(), 'html', 'utf-8')
    enclosure1["Content-Type"] = 'application/octet-stream'
    enclosure1["Content-Disposition"] = 'attachment; filename=report.html'
    message.attach(enclosure1)
    return message

def sendreport():
    #发送邮件
    try:
        smtp = smtplib.SMTP_SSL(mail_host, 465)
        smtp.login(mail_from, mail_password)
        message = email_content()
        smtp.sendmail(mail_from, mail_to, message.as_string())
        smtp.quit()
        print("email has send out!")
    except smtplib.SMTPException:
        print("email send error!")

