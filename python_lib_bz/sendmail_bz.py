#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado_template
import smtplib

loader = tornado_template.Loader("email_template")

mail_server = 'smtp.exmail.qq.com'
mail_port = 25
#mail_user = "hold@highwe.com"
#mail_pwd = "highwe123"


def sendMail(mail_to, content, mail_user, mail_pwd):
    '''
    modify by bigzhu at 15/04/28 11:31:53 去掉 try
    modify by bigzhu at 15/04/28 11:36:37 mail_user mail_pwd 改为传入参数
    '''
    smtp = smtplib.SMTP()
    smtp.connect(mail_server, mail_port)
    smtp.login(mail_user, mail_pwd)
    smtp.sendmail(mail_user, mail_to, content.as_string())
    smtp.quit()
