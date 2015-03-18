#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado_template
import pg
import smtplib
import time
import public

loader = tornado_template.Loader("email_template")

mail_server = 'smtp.exmail.qq.com'
mail_port = 25
mail_user = "hold@highwe.com"
mail_pwd = "*highwe123"

def sendMail(mail_to, content):
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_server, mail_port)
        smtp.login(mail_user, mail_pwd)
        smtp.sendmail(mail_user, mail_to, content.as_string())
        smtp.quit()
    except Exception as e:
        print "sendMail Exception:", e
