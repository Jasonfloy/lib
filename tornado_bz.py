#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
tornado 相关的公用代码
'''

import tornado
import os
import public_bz


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
    print public_bz.getExecutingPath()
    settings = {
        'static_path': os.path.join(public_bz.getExecutingPath(), 'static'),
        'debug': debug,
        'cookie_secret': 'bigzhu so big',
        'autoescape': None, # 模板自定义转义
        'login_url': "/login"
    }

    application = tornado.web.Application(url_map, **settings)
    return application


if __name__ == '__main__':
    pass
