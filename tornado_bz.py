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


def getURLMap(the_globals):
    '''
        根据定义的tornado.web.RequestHandler,自动生成url map
    '''
    url_map = []
    for i in the_globals:
        try:
            if issubclass(the_globals[i], tornado.web.RequestHandler):
                url_map.append((r'/' + i, the_globals[i]))
                url_map.append((r"/%s/([0-9]+)" % i, the_globals[i]))
        except TypeError:
            continue
    return url_map


def getApplication(url_map, debug=True):
    '''
        返回 tornado 的 application,有一些默认值,省得每次都设置:
            debug:  True 则开启调试模式,代码自动部署,但是有语法错误,会导致程序 cash
            login_url: 装饰器 tornado.web.authenticated 未登录时候,重定向的网址
    '''
    settings = {
        'static_path': os.path.join(public_bz.getExecutingPath(), 'static'),
        'debug': debug,
        'cookie_secret': 'bigzhu so big',
        'autoescape': None,  # 模板自定义转义
        'login_url': "/login",
        'ui_modules': tornado_ui_bz
    }

    application = tornado.web.Application(url_map, **settings)
    return application


def getTName(self):
    '''
    取得模板的名字
    与类名保持一致
    '''
    return 'template/' + self.__class__.__name__ + '.html'


def handError(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)
        except Exception:
            self.write(json.dumps({'error': public_bz.getExpInfo()}))
            print public_bz.getExpInfoAll()
    return wrapper

if __name__ == '__main__':
    pass
