#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
create by bigzhu at 15/06/29 14:03:23 注册
'''
from ui_module import my_ui_module
from tornado_bz import UserInfoHandler
import tornado_bz
import json
import user_bz
import validate_bz


class signup_m(my_ui_module.MyUIModule):

    '''
    create by bigzhu at 15/06/29 14:01:12 注册
    '''

    def render(self, user_types=[], btn_color='btn-primary' ):
        user_name = self.handler.get_argument('user_name', None)
        email = ''
        if user_name:
            if validate_bz.validateEmail(user_name):
                email = user_name
        else:
            user_name = ''
        return self.render_string(self.html_name, user_types=user_types, user_name=user_name, email=email, btn_color=btn_color)

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


class signup(UserInfoHandler):

    def initialize(self):
        UserInfoHandler.initialize(self)
        self.user_oper = user_bz.UserOper(self.pg)

    def get(self):
        self.render(tornado_bz.getTName(self))

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        login_info = json.loads(self.request.body)

        user_name = login_info.get("user_name")
        password = login_info.get("password")
        email = login_info.get("email")
        # 用户是否存在应该注册提交前判断,这里再次判断
        user_info = self.user_oper.getUserInfo(user_name=user_name)
        if user_info:
            raise Exception('用户已经存在, 请换一个用户名')
        user_info = self.user_oper.getUserInfo(email=email)
        if user_info:
            raise Exception('邮箱已经被使用, 请更换一个邮箱')

        user_type = login_info.get("user_type", 'my')

        self.user_oper.signup(user_name, password, email, user_type)
        user_info = self.user_oper.login(user_name, password, "'%s'" % user_type)
        self.set_secure_cookie("user_id", str(user_info.id))
        self.write(json.dumps({'error': '0'}))

if __name__ == '__main__':
    pass
