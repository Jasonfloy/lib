#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/06/29 14:03:23 注册
'''
from ui_module import my_ui_module
from tornado_bz import BaseHandler
import tornado_bz
import json
import user_bz
import hashlib


class reset_password_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/06/30 08:29:05 for reset password
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


class reset_password(BaseHandler):

    '''
    create by bigzhu at 15/06/29 21:45:22 找回密码
    modify by bigzhu at 15/06/30 09:08:29 已经登录用户如果要修改密码,必须输入老密码,暂时取消这个功能
    '''

    def initialize(self):
        BaseHandler.initialize(self)
        self.user_oper = user_bz.UserOper(self.pg)

        self.salt = "hold is watching you"

    def get(self, token):
        self.render(tornado_bz.getTName(self))

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        data = json.loads(self.request.body)

        password = data.get("password")
        token = data.get("token")

        hashed_password = hashlib.md5(password + self.salt).hexdigest()
        ##用已经登录用户直接修改密码
        #if self.current_user:
        #    count = self.pg.db.update('user_info', where="id = %s" % self.current_user, password=hashed_password, forget_token='')
        #    if count == 0:
        #        raise Exception('没有这个用户')
        #else:
        ##token 找回密码
        count = self.pg.db.update('user_info', where="forget_token = '%s'" % token, password=hashed_password, forget_token='')
        if count == 0:
            raise Exception('非法的修改密码请求!如有疑议,请联系管理员')
        self.write(json.dumps({'error': '0'}))

if __name__ == '__main__':
    pass
