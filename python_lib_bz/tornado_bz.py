#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
tornado 相关的公用代码
'''

import tornado
import os
import public_bz
import tornado_ui_bz
import functools
import json


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.pg = self.settings['pg']

    def get_current_user(self):
        return self.get_secure_cookie("user_id")


def getURLMap(the_globals):
    '''
        根据定义的tornado.web.RequestHandler,自动生成url map
    '''
    url_map = []
    for i in the_globals:
        try:
            if issubclass(the_globals[i], tornado.web.RequestHandler):
                url_map.append((r'/' + i, the_globals[i]))
                #url_map.append((r"/%s/([0-9]+)" % i, the_globals[i]))
                url_map.append((r"/%s/(.*)" % i, the_globals[i]))
        except TypeError:
            continue
    return url_map


def getSettings():
    '''
        返回 tornado 的 settings ,有一些默认值,省得每次都设置:
            debug:  True 则开启调试模式,代码自动部署,但是有语法错误,会导致程序 cash
            ui_modules 自定义的 ui 模块,默认会引入 tornado_ui_bz
            login_url: 装饰器 tornado.web.authenticated 未登录时候,重定向的网址
    '''
    settings = {
        'static_path': os.path.join(public_bz.getExecutingPath(), 'static'),
        'debug': True,
        'cookie_secret': 'bigzhu so big',
        'autoescape': None,  # 模板自定义转义
        'login_url': "/login",
        'ui_modules': []
    }
    return settings


def getTName(self, name=None):
    '''
    取得模板的名字
    与类名保持一致
    '''
    if name:
        return 'template/' + name + '.html'
    else:
        return 'template/' + self.__class__.__name__ + '.html'


def handleError(method):
    '''
    出现错误的时候,用json返回错误信息回去
    很好用的一个装饰器
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)
        except Exception:
            self.write(json.dumps({'error': public_bz.getExpInfo()}))
            print public_bz.getExpInfoAll()
    return wrapper


def mustLogin(method):
    '''
    必须要登录,否则弹回登录页面
    很好用的一个装饰器
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            pass
        else:
            self.redirect("/login")
            return
        method(self, *args, **kwargs)
    return wrapper


def getUserId(request):
    '''
    获取当前 user_id
    未登录则为 1
    '''
    user_id = request.current_user
    if user_id:
        pass
    else:
        user_id = 1
    return user_id
if __name__ == '__main__':
    pass
