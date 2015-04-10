#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import UIModule
action = ''
JS_PATH = "/lib_static/js/"
CSS_PATH = "/lib_static/css/"


class MyUIModule(UIModule):

    '''
    modify by bigzhu at 15/03/06 17:04:03 加入file
    create by bigzhu at 15/03/07 21:12:30 改成 file 了,没法用模板了
    '''

    def __init__(self, handler):
        UIModule.__init__(self, handler)
        self.pg = self.handler.settings['pg']

        self.class_name = self.__class__.__name__
        self.css_name = self.class_name + '.css'
        self.js_name = self.class_name + '.js'
        self.html_name = self.class_name + '.html'

        self.js_file = JS_PATH + self.js_name
        self.css_file = CSS_PATH + self.css_name

    def javascript_files(self):
        return self.js_file+'?v=1'

    def css_files(self):
        return self.css_file

    '''
    def embedded_css(self):
        return self.render_string(self.css_name)

    def embedded_javascript(self):
        return self.render_string(self.js_name, action_url=self.action_url)
    '''

    def render(self):
        return self.render_string(self.html_name)


class JsCssUIModule(UIModule):

    '''
    create by bigzhu at 15/02/22 03:40:44 用于只有 js 的 ui module
    modify by bigzhu at 15/02/22 21:30:12 public 还有 css 也得弄过去
    modify by bigzhu at 15/03/06 17:05:47 改为用 file
    '''

    def __init__(self, handler):
        UIModule.__init__(self, handler)
        self.pg = self.handler.settings['pg']

        self.class_name = self.__class__.__name__
        self.js_name = self.class_name + '.js'
        self.css_name = self.class_name + '.css'

        self.js_file = JS_PATH + self.js_name
        self.css_file = CSS_PATH + self.css_name

    def javascript_files(self):
        return self.js_file

    def css_files(self):
        return self.css_file

    '''
    def embedded_javascript(self):
        return self.render_string(self.js_name)

    def embedded_css(self):
        return self.render_string(self.css_name)
    '''

    def render(self):
        return ''


class HtmlUIModule(UIModule):

    '''
    create by bigzhu at 15/03/05 10:22:54 只要返回 html 就可以了
    '''

    def __init__(self, handler):
        UIModule.__init__(self, handler)
        self.pg = self.handler.settings['pg']

        self.class_name = self.__class__.__name__
        self.html_name = self.class_name + '.html'

    def embedded_javascript(self):
        return ''

    def embedded_css(self):
        return ''

    def render(self):
        return self.render_string(self.html_name)
