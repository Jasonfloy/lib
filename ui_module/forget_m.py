#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/06/29 14:03:23 注册-忘记密码
'''
from ui_module import my_ui_module
from tornado_bz import UserInfoHandler
import tornado_bz
import json
import user_bz
import uuid
from email.MIMEText import MIMEText
from sendmail_bz import sendMail


class forget_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/06/29 14:01:12 find password
    '''

    def render(self):
        return self.render_string(self.html_name)

    def javascript_files(self):
        my_js_files = [
            self.LIB_PATH + 'jquery-toastmessage-plugin/src/main/javascript/jquery.toastmessage.js',
            self.js_file
        ]
        self.all_js_files += my_js_files

        return self.all_js_files

    def css_files(self):
        my_css_files = [
            self.LIB_PATH + 'jquery-toastmessage-plugin/src/main/resources/css/jquery.toastmessage.css',
            self.css_file
        ]
        self.all_css_files += my_css_files
        return self.all_css_files


class forget(UserInfoHandler):

    '''
    create by bigzhu at 15/06/29 21:45:22 找回密码
    '''

    def initialize(self):
        UserInfoHandler.initialize(self)
        self.user_oper = user_bz.UserOper(self.pg)

        self.mail_name = 'hold@highwe.com'  # 用什么邮件来发送
        self.mail_password = 'highwe123'  # 邮件密码

    def get(self):
        self.render(tornado_bz.getTName(self))

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        login_info = json.loads(self.request.body)

        email = login_info.get("email")
        user_info = self.user_oper.getUserInfo(email=email)
        if not user_info:
            raise Exception('没有邮箱为%s的用户!' % email)
        forget_token = str(uuid.uuid4())

        sql_set_token = "update user_info set forget_token = '%s' where email = '%s' and user_type = 'my'" % (forget_token, email)
        self.pg.db.query(sql_set_token)
        url = 'http://' + self.request.host + '/reset_password/' + forget_token
        # content = MIMEText(loader.load("login_email_m.html").generate(user_name=email, url=url), 'html', 'utf-8')
        content = MIMEText('<a href="' + url + '">点此设置新密码</a><br><br>如果以上按钮点击无效，请将链接复制到浏览器地址栏中打开：<br>' + url, 'html', 'utf-8')
        content['From'] = self.mail_name
        content['To'] = email

        content['Subject'] = '找回密码'
        send_mail = self.settings.get('send_mail', self.mail_name)
        sendMail(email, content, send_mail, self.mail_password)
        self.write(json.dumps({'error': '0'}))

if __name__ == '__main__':
    pass
